#!/usr/bin/python

# iWidget application for openmeteo Enhydris software
# This software is provided with the AGPL license
# Copyright (c) 2013 National Techincal University of Athens

# This is the process_data management command that it can be
# dispatched automatically in regular intervals to process raw time
# series data and to calculated aggregated data.

import math
from datetime import datetime

from django.core.management.base import BaseCommand
from django.db import transaction
from django import db

from enhydris.hcore.models import ReadTimeStep
from iwidget.models import (Household, TSTEP_FIFTEEN_MINUTES,
        TSTEP_DAILY, TSTEP_MONTHLY, TSTEP_HOURLY, DMA,
        VAR_PERIOD, VAR_COST, VAR_ENERGY_PERIOD, VAR_ENERGY_COST,
        VAR_CUMULATIVE, VAR_ENERGY_CUMULATIVE)
from iwidget.cost_calculation import (calculate_cost_timeseries,
        CUBIC_METER_FLAT_RATE, KWH_FLAT_RATE)
from pthelma.timeseries import timeseries_bounding_dates_from_db
from pthelma.timeseries import Timeseries as TSeries

def _dif_in_secs(d1, d2):
    """
    This is a helper function, calculating the difference in seconds
    between two timestamps
    """
    return float((d2-d1).days*86400+(d2-d1).seconds)

def regularize_raw_series(raw_series_db, proc_series_db, rs, re, ps, pe ):
    """
    This function regularize raw_series_db object from database and
    writes a processed proc_series_db in database.
    Raw series is a continuously increasing values time series,
    aggregating the water consumption. Resulting processed timeseries
    contains water consumption for each of its interval. I.e. if the
    timeseries is of 15 minutes time step, then each record contains
    the water consumption for each record period.
    """
    raw_series = TSeries(id=raw_series_db.id)
    raw_series.read_from_db(db.connection)
    # We keep the last value for x-checking reasons, see last print
    # command
    test_value = raw_series[raw_series.bounding_dates()[1]]
    time_step = ReadTimeStep(proc_series_db.id, proc_series_db)
    proc_series = TSeries(id=proc_series_db.id, time_step = time_step)
    # The following code can be used in real conditions to append only
    # new records to db, in a next version
    #if not pe:
    #    start = proc_series.time_step.down(rs)
    #else:
    #    start = proc_series.time_step.up(pe)
    # Instead of the above we use now:
    start = proc_series.time_step.down(rs)
    end = proc_series.time_step.up(re)
    pointer = start
    # Pass 1: Initialize proc_series
    while pointer<=end:
        proc_series[pointer] = float('nan')
        pointer = proc_series.time_step.next(pointer)
    # Pass 2: Transfer cummulative raw series to differences series:
    prev_s = 0
    for i in xrange(len(raw_series)):
        dat, value = raw_series.items(pos=i)
        if not math.isnan(value):
            raw_series[dat] = value-prev_s
            prev_s = value
    # Pass 3: Regularize step: loop over raw series records and distribute
    # floating point values to processed series
    for i in xrange(len(raw_series)):
        dat, value = raw_series.items(pos=i)
        if not math.isnan(value):
            # find previous, next timestamp of the proc time series
            d1 = proc_series.time_step.down(dat)
            d2 = proc_series.time_step.up(dat)
            if math.isnan(proc_series[d1]): proc_series[d1] = 0
            if math.isnan(proc_series[d2]): proc_series[d2] = 0
            if d1==d2: # if dat on proc step then d1=d2
                proc_series[d1] += value
                continue
            dif1 = _dif_in_secs(d1, dat)
            dif2 = _dif_in_secs(dat, d2)
            dif = dif1+dif2
            # Distribute value to d1, d2
            proc_series[d1] += (dif2/dif)*value
            proc_series[d2] += (dif1/dif)*value
    # Uncomment the following line in order to show debug information.
    # Usually the three following sums are consistent by equality. If
    # not equality is satisfied then there is a likelyhood of algorith
    # error
    print raw_series.sum(), proc_series.sum(), test_value
    proc_series.write_to_db(db=db.connection, commit=True) #False)
    #return the full timeseries
    return proc_series

def process_household(household, bounds):
    """
    Processes each household time series, first by regularizing step
    of the raw series to the fifteen minutes time series, then by
    aggregating fifteen minutes series to hourly, daily, monthly.
    """
    print "Processing household: %s"%(household.alt_codes.all()[0],)
    for variable in (VAR_PERIOD, VAR_ENERGY_PERIOD):
        raw_series_db = household.timeseries.filter(time_step__isnull=True,
                variable__id = {VAR_PERIOD: VAR_CUMULATIVE,
                    VAR_ENERGY_PERIOD: VAR_ENERGY_CUMULATIVE}[variable])[:1]
        if not raw_series_db:
            continue
        raw_series_db = raw_series_db[0]
        fifteen_min_series_db = household.timeseries.get(time_step__id=
                TSTEP_FIFTEEN_MINUTES, variable__id=variable)
        s1, e1 = timeseries_bounding_dates_from_db(db.connection,
                raw_series_db.id)
        s2, e2 = timeseries_bounding_dates_from_db(db.connection,
                fifteen_min_series_db.id)
    #    if e2 and (e1-e2).seconds<15*60:
    #        return
        fifteen_min_series = regularize_raw_series(raw_series_db,
                fifteen_min_series_db, s1,e1,s2,e2)
        if fifteen_min_series.bounding_dates():
            bounds[variable]['fifteen_start'] = min(
                    bounds[variable]['fifteen_start'],
                    fifteen_min_series.bounding_dates()[0])
            bounds[variable]['fifteen_end'] = max(
                    bounds[variable]['fifteen_end'],
                    fifteen_min_series.bounding_dates()[1])
        result = fifteen_min_series
        monthly_series = None
        for time_step_id in (TSTEP_HOURLY, TSTEP_DAILY, TSTEP_MONTHLY):
            if not result:
                break
            result = aggregate_household_series(bounds, household,
                    result, time_step_id, variable)
            if time_step_id == TSTEP_MONTHLY:
                monthly_series = result
        if not monthly_series:
            return
        # Cost calculation only if monthly_series present
        cost_timeseries_db = household.timeseries.get(time_step__id =
                TSTEP_MONTHLY, variable__id = 
                {VAR_PERIOD: VAR_COST,
                 VAR_ENERGY_PERIOD: VAR_ENERGY_COST
                }[variable])
        cost_timeseries = calculate_cost_timeseries(monthly_series,
                rate = {
                    VAR_PERIOD: CUBIC_METER_FLAT_RATE,
                    VAR_ENERGY_PERIOD: KWH_FLAT_RATE}[variable])
        cost_timeseries.id = cost_timeseries_db.id
        cost_timeseries.write_to_db(db = db.connection, commit=True)
    
def aggregate_household_series(bounds, household, source_time_series,
        dest_timestep_id, variable):
    MISSING_ALLOWED = {
        TSTEP_HOURLY: 4,
        TSTEP_DAILY: 12,
        TSTEP_MONTHLY: 15
    }
    BOUNDS = {
        TSTEP_HOURLY: ('hourly_start', 'hourly_end'),
        TSTEP_DAILY: ('daily_start', 'daily_end'),
        TSTEP_MONTHLY: ('monthly_start', 'monthly_end')
    }
    dest_timeseries_db = household.timeseries.get(time_step__id =
            dest_timestep_id, variable__id=variable)
    dest_time_step = ReadTimeStep(dest_timeseries_db.id,
            dest_timeseries_db)
    if not source_time_series.bounding_dates():
        return
    dest_timeseries = source_time_series.aggregate(
            target_step = dest_time_step,
            missing_allowed = MISSING_ALLOWED[dest_timestep_id],
            missing_flag = 'MISSING')[0]
    dest_timeseries.id = dest_timeseries_db.id
    dest_timeseries.write_to_db(db = db.connection, commit=True)
    for i, func in ((0, min),(1, max)):
        if not dest_timeseries.bounding_dates():
            break
        bounds[variable][BOUNDS[dest_timestep_id][i]] = func(
                bounds[variable][BOUNDS[dest_timestep_id][i]],
                dest_timeseries.bounding_dates()[i])
    return dest_timeseries

def process_dma(dma, bounds):
    """Process DMA timeseries by aggregating all the contained
    households in the DMA"""
    print "Process DMA %s"%(dma,)
    for dma_series in dma.timeseries.all():
        print "Process series %s"%(dma_series,)
        per_capita = dma_series.name.find('capita')>-1
        variable = dma_series.variable.id
        if dma_series.time_step.id == TSTEP_FIFTEEN_MINUTES:
            start = bounds[variable]['fifteen_start']
            end = bounds[variable]['fifteen_end']
            # Fifteen minutes process is DEACTIVATED!
            # We don't process fifteen minutes, it takes too long,
            # maybe we reactivate later after we optimize the
            # algorithm to process only new records
            continue
        elif dma_series.time_step.id == TSTEP_HOURLY:
            start = bounds[variable]['hourly_start']
            end = bounds[variable]['hourly_end']
        elif dma_series.time_step.id == TSTEP_DAILY:
            start = bounds[variable]['daily_start']
            end = bounds[variable]['daily_end']
        elif dma_series.time_step.id == TSTEP_MONTHLY:
            start = bounds[variable]['monthly_start']
            end = bounds[variable]['monthly_end']
        time_step = ReadTimeStep(dma_series.id, dma_series)
        tseries = TSeries(time_step = time_step, id=dma_series.id)
        nhseries = TSeries(time_step = time_step)
        pointer = start
        while pointer<=end:
            tseries[pointer] = 0
            nhseries[pointer] = 0
            pointer = tseries.time_step.next(pointer)
        for household in dma.households.all():
            for h_series_db in household.timeseries.filter(
                    time_step__id=dma_series.time_step.id,
                    variable__id=variable):
                hseries = TSeries(id=h_series_db.id)
                hseries.read_from_db(db.connection)
                pointer = start
                while pointer<=end:
                    try:
                        v = hseries[pointer]
                        if math.isnan(v):
                            pointer = tseries.time_step.next(pointer)
                            continue
                        if per_capita:
                            v = v/float(household.num_of_occupants)
                        tseries[pointer] += v
                        nhseries[pointer] += 1
                    except KeyError:
                        v = 0
                    pointer = tseries.time_step.next(pointer)
        pointer = start
        while pointer<=end:
            if per_capita and nhseries[pointer]>0:
                tseries[pointer] = tseries[pointer] / nhseries[pointer]
            pointer = tseries.time_step.next(pointer)
        tseries.write_to_db(db.connection, commit=True)#False)

# These are some Time limits used as a starting point for the actual
# start and end date lookup function
MAX_DATE = datetime(2100,1,1,0,0,0)
MIN_DATE = datetime(1900,1,1,0,0,0)

class Command(BaseCommand):
    args = ''
    help = 'Process raw series to complete 15 minutes series, then '\
           'performs aggregation'

    def handle(self, *args, **options):
        options['handle'] = self
        bounds ={
                VAR_PERIOD:
                    {'fifteen_start': MAX_DATE, 'fifteen_end': MIN_DATE,
                    'hourly_start': MAX_DATE, 'hourly_end': MIN_DATE,
                    'daily_start': MAX_DATE, 'daily_end': MIN_DATE,
                    'monthly_start': MAX_DATE, 'monthly_end': MIN_DATE},
                VAR_ENERGY_PERIOD:
                    {'fifteen_start': MAX_DATE, 'fifteen_end': MIN_DATE,
                    'hourly_start': MAX_DATE, 'hourly_end': MIN_DATE,
                    'daily_start': MAX_DATE, 'daily_end': MIN_DATE,
                    'monthly_start': MAX_DATE, 'monthly_end': MIN_DATE}}
        for household in Household.objects.all():
            # We "commit" to database each household, if everything
            # went ok. Write some action on failures and
            # exceptions, maybe the whole process should be under one
            # big transaction, or oposite solution: on exception
            # ignore and continue to other households, log the error.
            with transaction.commit_on_success():
                process_household(household, bounds)
        for dma in DMA.objects.all():
            # The same holds for DMAs (see above)
            with transaction.commit_on_success():
                process_dma(dma, bounds)
