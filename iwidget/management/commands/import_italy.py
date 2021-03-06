#!/usr/bin/python

# iWidget application for openmeteo Enhydris software
# This software is provided with the AGPL license
# Copyright (c) 2013-2014 National Techincal University of Athens

# This command is to import real data from the Portugal application to
# test the concept version of iWidget.
# This is a modified version of ``import_portugal.py`` which is reading
# a sole CSV file with Italy data
#

from datetime import datetime
import math
from optparse import make_option
import os
import random

from django import db
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from iwidget.models import (DMA, Household, IWTimeseries,
        CUBIC_METERS, TZONE_UTC, VAR_CUMULATIVE,
        VAR_ENERGY_CUMULATIVE, UNIT_KILOWATTHOUR,
        VAR_PERIOD, TSTEP_FIFTEEN_MINUTES, TSTEP_DAILY,
        TSTEP_MONTHLY, TSTEP_HOURLY, VAR_COST, UNIT_EURO,
        VAR_ENERGY_PERIOD, VAR_ENERGY_COST,
        GENTITYALTCODETYPE,)

from pthelma.timeseries import Timeseries as TSeries
from pthelma.timeseries import timeseries_bounding_dates_from_db
from pthelma.timeseries import IntervalType

AVERAGE_UNIT_WATER_CONSUMPTION = 100.000
"""
This parameter will be used to estimate the occupancy of each
household on import
"""

def _parse_line(line):
    """
    Parses line ``line`` where line is a string  and returns a dictionary with
    components. If impossible to parse, returns None
    """
    components = line.split('/',1)
    if not components or len(components)!=2:
        return
    preable = components[0]
    main_container = components[1]
    components = preable.split('_',2)
    if not components or len(components)!=3:
        return
    household = components[2]
    components = main_container.split(',')
    if not components or len(components)!=5:
        return
    variable_type = components[0]
    assert variable_type in ('Electricity', 'WaterCold', 'WaterHot')
    datestr = components[1]
    timestamp = datetime.strptime(datestr, '%Y/%m/%d %H:%M')
    try:
        value = float(components[3])
    except ValueError:
        value = float('NaN')
    return {
            'household': household,
            'variable_type': variable_type,
            'timestamp': timestamp,
            'value': value}

def read_file(filename, dma, force=False):
    """
    Reads file ``filename`` line by line and when household changes
    calls a function to create database objects for household, user
    and time series.

    Set force to True to .... TODO write
    """

    def initialize_series():
        return dict(WaterCold=[], WaterHot=[], Electricity=[])

    household = None
    series = initialize_series()
    with open(filename, 'rt') as fp:
        for line in fp:
            parsed = _parse_line(line)
            if not parsed:
                continue
            if household and household != parsed['household']:
                # household changed, call the function to create database
                # objects, to save time series in db etc.
                create_objects(dma, household, series)
                series = initialize_series()
            household = parsed['household']
            series[parsed['variable_type']].append((
                    parsed['timestamp'], parsed['value']))
    # Call the same function here to deal with last household
    create_objects(dma, household, series, force)

def create_objects(dma, household_identifier, series, force=False):
    """
    When a household is fully parsed then this command is called to create
    database objects thus: user (household owner), household, database time
    series placeholders (for raw data and for processed data), to write actual
    time series data in database and finally to estimate the household
    occupancy.
    """
    print "Processing household %s, user username will be %s as well"%(
            household_identifier, household_identifier)
    # Create user (household owner), household, database series placeholders
    user = create_user(household_identifier)
    household=create_household(household_identifier, user,
            zone=dma.id)
    db_series = create_raw_timeseries(household)
    create_processed_timeseries(household)
    timeseries_data = {}
    # Now we will create timeseries.Timeseries() and we will add
    # parsed values
    for variable in db_series:
        if variable not in ('WaterCold', 'Electricity'):
            continue
        s, e = timeseries_bounding_dates_from_db(db.connection,
                db_series[variable].id)
        if not force and (s or e):
            print 'Raw timeseries id=%s has already data, skipping...'%(
                    db_series[variable].id,)
            continue
        timeseries = TSeries()
        timeseries.id = db_series[variable].id
        total = 0.0
        for timestamp, value in series[variable]:
            if not math.isnan(value):
                total += value
                timeseries[timestamp] = total
            else:
                timeseries[timestamp] = float('NaN')
        timeseries_data[variable] = timeseries
        timeseries.write_to_db(db=db.connection,
                transaction=transaction,
                commit=False)
    if 'WaterCold' in timeseries_data:
        calc_occupancy(timeseries_data['WaterCold'], household)

def calc_occupancy(timeseries, household):
    """
    Now it is time to estimate household occupancy, we use the
    total_timeseries, we find the last not-null value and the first not-null
    and non-zero value. We calculate the time interval between those two
    values and finally find an average per day consumption.
    """
    count = len(timeseries)
    if not count:
        return
    first_record = None
    last_record = None
    i = 0
    while i<count:
        timestamp, value = timeseries.items(pos=i)
        if not math.isnan(value) and value>0.0:
            first_record = timestamp, value
            break
        i += 1
    i = count-1
    while i>=0:
        timestamp, value = timeseries.items(pos=i)
        if not math.isnan(value):
            last_record = timestamp, value
            break
        i -= 1
    if first_record and last_record:
        diff = float((last_record[0]-first_record[0]).days)
        average_consumption = last_record[1]*1000.0 / diff
        num_of_occupants = max(1,
                int(round(average_consumption/AVERAGE_UNIT_WATER_CONSUMPTION)))
        print 'Estimated number of occupants: %s'%(num_of_occupants,)
        household.num_of_occupants = num_of_occupants
        household.save()

def create_user(identifier):
    """Identifier will be used as username == household name"""
    try:
        return User.objects.get(username=identifier)
    except User.DoesNotExist:
        pass
    u = User.objects.create(username=identifier,
            first_name = 'Unspecified',
            last_name = 'Unspecified',
            is_staff = False, is_active = True, is_superuser = False,
            email = identifier+'@example.com')
    u.set_password('iwidgetuser')
    u.save()
    u.profile.fname = u.first_name
    u.profile.lname = u.last_name
    u.profile.save()
    return u

def create_household(identifier, user, zone):
    try:
        return Household.objects.get(user=user)
    except Household.DoesNotExist:
        pass
    dma = DMA.objects.get(pk=zone)
    household = Household.objects.create(
            user = user,
            dma = dma,
            property_type_id=1,
            num_of_occupants = random.randint(1, 5),
            address = 'Somewhere')
    # We also create an "alternative" id entry based on the given
    # identifier, for future use
    household.alt_codes.create(type_id = GENTITYALTCODETYPE,
            value = identifier.lstrip('0'))
    return household

def create_raw_timeseries(household):
    db_series = {}
    for variable, unit in [(VAR_CUMULATIVE, CUBIC_METERS),
            (VAR_ENERGY_CUMULATIVE, UNIT_KILOWATTHOUR)]:
        try:
            series = IWTimeseries.objects.get(gentity=household,
                    time_step__isnull=True,
                    variable=variable)
            db_series[variable] = series
            continue
        except IWTimeseries.DoesNotExist:
            pass
        series = IWTimeseries.objects.create(
                gentity=household,
                variable_id=variable,
                time_zone_id = TZONE_UTC,
                unit_of_measurement_id = unit,
                name = 'Cumulative water consumption'
                )
        db_series[{
                VAR_CUMULATIVE: 'WaterCold',
                VAR_ENERGY_CUMULATIVE: 'Electricity'}
                        [variable]] = series
    return db_series

def create_processed_timeseries(household):
    # nominal_offset_minutes, _months, actual_offset_minutes, _months,
    # name
    tseries_list = [
            (TSTEP_FIFTEEN_MINUTES, 0,0,0,0, 'Fifteen minutes consumption',VAR_PERIOD),
            (TSTEP_HOURLY, 0,0,0,0,'Hourly consumption',VAR_PERIOD),
            (TSTEP_DAILY, 0,0,1440,0,'Daily consumption',VAR_PERIOD),
            (TSTEP_MONTHLY, 0,0,0,1,'Monthly consumption',VAR_PERIOD),
            (TSTEP_FIFTEEN_MINUTES, 0,0,0,0, 'Fifteen minutes energy consumption',VAR_ENERGY_PERIOD),
            (TSTEP_HOURLY, 0,0,0,0,'Hourly energy consumption',VAR_ENERGY_PERIOD),
            (TSTEP_DAILY, 0,0,1440,0,'Daily energy consumption',VAR_ENERGY_PERIOD),
            (TSTEP_MONTHLY, 0,0,0,1,'Monthly energy consumption',VAR_ENERGY_PERIOD),
            (TSTEP_MONTHLY, 0,0,0,1,'Monthly cost',VAR_COST),
            (TSTEP_MONTHLY, 0,0,0,1,'Monthly energy cost',VAR_ENERGY_COST),
    ]
    for ts in tseries_list:
        variable_id = ts[6]
        time_step_id = ts[0]
        unit_of_measurement_id = {
                    VAR_COST: UNIT_EURO,
                    VAR_ENERGY_COST: UNIT_EURO,
                    VAR_PERIOD: CUBIC_METERS,
                    VAR_ENERGY_PERIOD: UNIT_KILOWATTHOUR}[variable_id]
        if IWTimeseries.objects.filter(gentity=household,
                time_step__id=time_step_id,
                variable__id=variable_id).exists():
            continue
        ts_object = IWTimeseries.objects.create(
                time_step_id = time_step_id,
                gentity=household,
                variable_id=variable_id,
                interval_type_id = IntervalType.SUM,
                time_zone_id = TZONE_UTC,
                unit_of_measurement_id = unit_of_measurement_id,
                name = ts[5],
                nominal_offset_minutes = ts[1],
                nominal_offset_months = ts[2],
                actual_offset_minutes = ts[3],
                actual_offset_months = ts[4],
                )
        assert ts_object

def create_dma_series(zone):
    print 'Create zone id=%s timeseries'%(zone,)
    # nominal_offset_minutes, months, actual_offset_minutes, months
    # name, variable, munit
    tseries_list = {
        (TSTEP_HOURLY, VAR_PERIOD): [0,0,0,0,'Hourly consumption', VAR_PERIOD,
                                     CUBIC_METERS],
        (TSTEP_DAILY, VAR_PERIOD): [0,0,1440,0,'Daily consumption', VAR_PERIOD,
                                    CUBIC_METERS],
        (TSTEP_MONTHLY, VAR_PERIOD): [0,0,0,1,'Monthly consumption', VAR_PERIOD,
                                      CUBIC_METERS],
        (TSTEP_HOURLY, VAR_ENERGY_PERIOD): [0,0,0,0,'Hourly energy', VAR_ENERGY_PERIOD,
                                            UNIT_KILOWATTHOUR],
        (TSTEP_DAILY, VAR_ENERGY_PERIOD): [0,0,1440,0,'Daily energy', VAR_ENERGY_PERIOD,
                                           UNIT_KILOWATTHOUR],
        (TSTEP_MONTHLY, VAR_ENERGY_PERIOD): [0,0,0,1,'Monthly energy', VAR_ENERGY_PERIOD,
                                             UNIT_KILOWATTHOUR],
    }
    skipped = True
    for ts in tseries_list:
        for per_capita in (False, True):
            time_step_id = ts[0]
            variable_id = ts[1]
            name = tseries_list[ts][4]
            exists_qs = IWTimeseries.objects.filter(gentity__id=zone,
                    time_step__id=time_step_id,
                    variable__id=variable_id)
            if per_capita:
                name = name + ' - per capita'
                exists_qs = exists_qs.filter(name__icontains='capita')
            if exists_qs.exists():
                continue
            skipped = False
            variable = tseries_list[ts][5]
            unit = tseries_list[ts][6]
            ts_object = IWTimeseries.objects.create(
                    time_step_id = time_step_id,
                    gentity_id=zone,
                    variable_id=variable,
                    interval_type_id = IntervalType.SUM,
                    time_zone_id = TZONE_UTC,
                    unit_of_measurement_id = unit,
                    name = name,
                    nominal_offset_minutes = tseries_list[ts][0],
                    nominal_offset_months = tseries_list[ts][1],
                    actual_offset_minutes = tseries_list[ts][2],
                    actual_offset_months = tseries_list[ts][3],
                    )
            assert ts_object
    if skipped:
        print 'Skipped...'

def create_zone():
    """
    We create a hard coded DMA containing the word 'Italy'
    """
    zones = DMA.objects.filter(name__icontains='italy')[:1]
    if zones:
        return zones[0]
    dma = DMA.objects.create(name='Italy electric-water')
    print 'Created DMA: "'+dma.name+" with id="+str(dma.id)
    return dma


class Command(BaseCommand):
    args = '<filename>'
    help = 'Imports time series data for the case of Italy'

    option_list = BaseCommand.option_list + (
        make_option('--force-overwrite',
            action='store_true',
            default=False,
            dest='force_overwrite',
            help='When specified, time series data are overwriten even '
                 'they exist from a previous calculation',
        ),)

    def handle(self, *args, **options):
        if len(args)!=1:
            raise CommandError('A Filename and only one filename should be '
                    'specified')
        filename = args[0]
        if not os.path.exists(filename):
            raise CommandError('File: %s does not exist'%filename)
        options['handle'] = self
        force_overwrite = options['force_overwrite']
        # maybe improve transaction control, is this has a
        # meaning, as this command is only for demonstration - concept
        # edition of the iWidget
        with transaction.commit_manually():
            try:
                dma = create_zone()
                create_dma_series(dma.id)
                read_file(filename, dma, force=force_overwrite)
                transaction.commit()
            except:
                transaction.rollback()
                raise

