#!/usr/bin/python

# iWidget application for openmeteo Enhydris software
# This software is provided with the AGPL license
# Copyright (c) 2013-2014 National Techincal University of Athens

# This command is to import real data from the Portugal application to
# test the concept version of iWidget.
# This is a modified version of ``import_portugal.py`` which is using
# the IBM REST API instead the CSV files
#

from os import listdir
import os.path
from datetime import datetime
import random

from django.core.management.base import BaseCommand, CommandError
from django import db
from django.db import transaction

from iwidget.models import DMA, Household, IWTimeseries
from iwidget import ibm_restapi

from pthelma.timeseries import Timeseries as TSeries
from pthelma.timeseries import timeseries_bounding_dates_from_db

def parse_and_save_timeseries(device_id, timeseries_id):
    """
    Reads a RAW timeseries from REST API and saves in our local
    database using the timeseries_id.
    ``device_id`` will be the ``identifier`` used in other functions,
    usualy is the customerID==deviceID
    """
    s, e = timeseries_bounding_dates_from_db(db.connection,
            timeseries_id)
    if s or e:
        print 'Raw timeseries id=%s has already data, skipping...'%(
                timeseries_id,)
        return
    timeseries = TSeries()
    timeseries.id = timeseries_id
    for timestamp, value in ibm_restapi.get_raw_timeseries(device_id):
        timeseries[timestamp] = value
    timeseries.write_to_db(db=db.connection,
            transaction=transaction,
            commit=False)

def create_user(identifier):
    """Identifier will be used as username == household name"""
    from django.contrib.auth.models import User
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
    from iwidget.models import GENTITYALTCODETYPE
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
    try:
        return IWTimeseries.objects.get(gentity=household,
            time_step__isnull=True)
    except IWTimeseries.DoesNotExist:
        pass
    from iwidget.models import (CUBIC_METERS, TZONE_UTC,
            VAR_CUMULATIVE)
    raw_timeseries = IWTimeseries.objects.create(
            gentity=household,
            variable_id=VAR_CUMULATIVE,
            time_zone_id = TZONE_UTC,
            unit_of_measurement_id = CUBIC_METERS,
            name = 'Cumulative water consumption'
            )
    return raw_timeseries

def create_processed_timeseries(household):
    from iwidget.models import (CUBIC_METERS, TZONE_UTC,
            VAR_PERIOD, TSTEP_FIFTEEN_MINUTES, TSTEP_DAILY,
            TSTEP_MONTHLY, TSTEP_HOURLY, VAR_COST, UNIT_EURO)
    from pthelma.timeseries import IntervalType
    # nominal_offset_minutes, _months, actual_offset_minutes, _months,
    # name
    tseries_list = [
            (TSTEP_FIFTEEN_MINUTES, 0,0,0,0,
                    'Fifteen minutes consumption',VAR_PERIOD),
            (TSTEP_HOURLY, 0,0,0,0,'Hourly consumption',VAR_PERIOD),
            (TSTEP_DAILY, 0,0,1440,0,'Daily consumption',VAR_PERIOD),
            (TSTEP_MONTHLY, 0,0,0,1,'Monthly consumption',VAR_PERIOD),
            (TSTEP_MONTHLY, 0,0,0,1,'Monthly cost',VAR_COST),
    ]
    for ts in tseries_list:
        variable_id = ts[6]
        time_step_id = ts[0]
        unit_of_measurement_id = UNIT_EURO if variable_id == \
                VAR_COST else CUBIC_METERS
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

def create_dma_series(zone):
    from iwidget.models import (CUBIC_METERS, TZONE_UTC,
            VAR_PERIOD, TSTEP_FIFTEEN_MINUTES, TSTEP_DAILY,
            TSTEP_MONTHLY, TSTEP_HOURLY,)
    from pthelma.timeseries import IntervalType
    print 'Create zone id=%s timeseries'%(zone,)
    # nominal_offset_minutes, months, actual_offset_minutes, months
    # name
    tseries_list = {
            TSTEP_FIFTEEN_MINUTES: [0,0,0,0,'Fifteen minutes consumption',],
            TSTEP_HOURLY: [0,0,0,0,'Hourly consumption'],
            TSTEP_DAILY: [0,0,1440,0,'Daily consumption'],
            TSTEP_MONTHLY: [0,0,0,1,'Monthly consumption'],
    }
    skipped = True
    for ts in tseries_list:
        for per_capita in (False, True):
            name = tseries_list[ts][4]
            exists_qs = IWTimeseries.objects.filter(gentity__id=zone,
                    time_step__id=ts)
            if per_capita:
                name = name + ' - per capita'
                exists_qs = exists_qs.filter(name__icontains='capita')
            if exists_qs.exists():
                continue
            skipped = False
            ts_object = IWTimeseries.objects.create(
                    time_step_id = ts,
                    gentity_id=zone,
                    variable_id=VAR_PERIOD,
                    interval_type_id = IntervalType.SUM,
                    time_zone_id = TZONE_UTC,
                    unit_of_measurement_id = CUBIC_METERS,
                    name = name,
                    nominal_offset_minutes = tseries_list[ts][0],
                    nominal_offset_months = tseries_list[ts][1],
                    actual_offset_minutes = tseries_list[ts][2],
                    actual_offset_months = tseries_list[ts][3],
                    )
    if skipped:
        print 'Skipped...'

def create_objects(identifier, zone):
    """
    Creates the required database objects for identifier in zone, but
    does not parse time series data.
    """
    user = create_user(identifier)
    household = create_household(identifier, user, zone)
    raw_timeseries = create_raw_timeseries(household)
    create_processed_timeseries(household)
    return {'raw_timeseries': raw_timeseries,
            'household': household,
            'user': user}

def process_households(dmas):
    """
    Process the whole households list creating:
    -database users
    -household entries
    -timeseries entries
    -parse timeseries data and write to database

    ``dmas`` should be the dictionary return by read_zones to create
    the household entities with the correct reference to DMA (zone).
    """
    devices = ibm_restapi.residential_devices()
    for device in devices:
        if device['parent'] not in dmas:
            raise ibm_restapi.APIIntegrityError('Household in '
                    'non-existing zone')
        identifier = device['id']
        zone = dmas[device['parent']]
        print 'Processing household '+identifier+', zone: '+\
                device['parent']
        kwargs = create_objects(identifier, zone)
        if kwargs and kwargs.get('raw_timeseries', None):
            parse_and_save_timeseries(identifier,
                    kwargs['raw_timeseries'].id)
        else:
            print 'Skip...'

def read_zones():
    """
    Read all zones, creates such instances in database, returns a
    dictionary with keys the zone ids as they are comming from the API
    and values our db ids.
    """
    zones = ibm_restapi.zone_devices()
    dmas = {}
    for zone in zones:
        dma = DMA.objects.get_or_create(
                name='{0} - {1}'.format(zone['name'], zone['id'])
                )[0]
        dmas[zone['id']] = dma.id
        print 'Created DMA: "'+dma.name+" with id="+str(dma.id)
    return dmas

class Command(BaseCommand):
    help = 'Imports time series data from IBM REST API'

    def handle(self, *args, **options):
        options['handle'] = self
        # TODO: maybe improve transaction control, is this has a
        # meaning, as this command is only for demonstration - concept
        # edition of the iWidget
        with transaction.commit_manually():
            try:
                dmas = read_zones()
                process_households(dmas)
                for zone in dmas.values():
                    create_dma_series(zone)
                transaction.commit()
            except:
                transaction.rollback()
                raise

