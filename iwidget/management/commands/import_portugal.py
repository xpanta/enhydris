#!/usr/bin/python

# iWidget application for openmeteo Enhydris software
# This software is provided with the AGPL license
# Copyright (c) 2013 National Techincal University of Athens

# This command is to import real data from the Portugal application to
# test the concept version of iWidget.
# For each of the CSV files, a user is create, a household, raw series
# as well as placeholder entries in database for processed series.
# Finally CSV data are parsed into raw series in database.
#
# Prerequired to execute command: Create DMA entries in database, e.g.
# with django:
# % python manage.py shell
# >>> from iwidget.models import DMA
# >>> dma = DMA.objects.create(name="DMA name")
# >>> print dma.id
# <the dma id is printed, keep it to dispatch this command>

from os import listdir
import os.path
from datetime import datetime
import random

from django.core.management.base import BaseCommand, CommandError
from django import db
from django.db import transaction

from iwidget.models import DMA, Household, IWTimeseries

from pthelma.timeseries import Timeseries as TSeries

MIN_VALUE = 0
MAX_VALUE = 100000

def parse_and_save_timeseries(filename, timeseries_id):
    first_line = True
    timeseries = TSeries()
    timeseries.id = timeseries_id
    with open(filename) as fp:
        for line in fp.readlines():
            if first_line:
                first_line = False
                continue
            components = line.split(',')
            date_str = components[1].strip('"')
            value_str = components[2].strip('"')
            value = float(value_str)
            if value<MIN_VALUE or value>=MAX_VALUE:
                value = float('nan')
            tstamp = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
            tstamp = tstamp.replace(second=0)
            timeseries[tstamp] = value
    timeseries.write_to_db(db=db.connection,
            transaction=transaction,
            commit=False)

FIRST_NAMES = ('John', 'George', 'Nick', 'Basil', 'Steve', 'Michael', 
        'Thodoris', 'Petros', 'Jack', 'James', 'Ludwig')
LAST_NAMES = ('Papadopoulos', 'Michael', 'Nikolaidis', 'Papas',
        'Jones', 'Smith', 'Nikolopoulos', 'Ioannidis',
        'Vassilopoulos', 'Fotopoulos', 'Kafetzoglou')

def create_user(identifier):
    """Identifier will be used as username == household name"""
    from django.contrib.auth.models import User
    if User.objects.filter(username=identifier).exists():
        return
    # Assign a fake but cool full name, just for fun!
    u = User.objects.create(username=identifier,
            first_name = FIRST_NAMES[random.randint(0, len(FIRST_NAMES)-1)],
            last_name = LAST_NAMES[random.randint(0, len(LAST_NAMES)-1)],
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
    if Household.objects.filter(user=user).exists():
        return
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
    if IWTimeseries.objects.filter(gentity=household,
            time_step__isnull=True).exists():
        return
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
            TSTEP_MONTHLY, TSTEP_HOURLY,)
    from pthelma.timeseries import IntervalType
    # nominal_offset_minutes, _months, actual_offset_minutes, _months,
    # name
    tseries_list = {
            TSTEP_FIFTEEN_MINUTES: [0,0,0,0,'Fifteen minutes consumption',],
            TSTEP_DAILY: [0,0,1440,0,'Daily consumption'],
            TSTEP_MONTHLY: [0,0,0,1,'Monthly consumption'],
            TSTEP_HOURLY: [0,0,0,0,'Hourly consumption'],
    }
    for ts in tseries_list:
        if IWTimeseries.objects.filter(gentity=household,
                time_step__id=ts).exists():
            continue
        ts_object = IWTimeseries.objects.create(
                time_step_id = ts,
                gentity=household,
                variable_id=VAR_PERIOD,
                interval_type_id = IntervalType.SUM,
                time_zone_id = TZONE_UTC,
                unit_of_measurement_id = CUBIC_METERS,
                name = tseries_list[ts][4],
                nominal_offset_minutes = tseries_list[ts][0],
                nominal_offset_months = tseries_list[ts][1],
                actual_offset_minutes = tseries_list[ts][2],
                actual_offset_months = tseries_list[ts][3],
                )

def create_dma_series(zone):
    from iwidget.models import (CUBIC_METERS, TZONE_UTC,
            VAR_PERIOD, TSTEP_FIFTEEN_MINUTES, TSTEP_DAILY,
            TSTEP_MONTHLY, TSTEP_HOURLY,)
    from pthelma.timeseries import IntervalType
    print 'Create zone %s timeseries'%(zone,)
    # nominal_offset_minutes, months, actual_offset_minutes, months
    # name
    tseries_list = {
            TSTEP_FIFTEEN_MINUTES: [0,0,0,0,'Fifteen minutes consumption',],
            TSTEP_DAILY: [0,0,1440,0,'Daily consumption'],
            TSTEP_MONTHLY: [0,0,0,1,'Monthly consumption'],
            TSTEP_HOURLY: [0,0,0,0,'Hourly consumption'],
    }
    skipped = True
    for ts in tseries_list:
        for per_capita in (False, True):
            name = tseries_list[ts][4]
            exists_qs = IWTimeseries.objects.filter(gentity=zone,
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
    if not user: return
    household = create_household(identifier, user, zone)
    if not household: return
    raw_timeseries = create_raw_timeseries(household)
    if not raw_timeseries: return
    create_processed_timeseries(household)
    return {'raw_timeseries': raw_timeseries,
            'household': household,
            'user': user}

def process_file(filename, dirname, zone):
    """
    Process each file by creating relevant objects:
    -database user
    -household entry
    -timeseries entries
    -parse timeseries data and write to databaes
    """
    identifier = filename.split('-')[0]
    print 'Processing household '+identifier
    filename = os.path.join(dirname, filename)
    kwargs = create_objects(identifier, zone)
    if kwargs and kwargs.get('raw_timeseries', None):
        parse_and_save_timeseries(filename, kwargs['raw_timeseries'].id)
    else:
        print 'Skip...'

class Command(BaseCommand):
    args = '<files_dir dma_id>'
    help = 'Imports time series data from portugal files'

    def handle(self, *args, **options):
        options['handle'] = self
        if len(args)!=2:
            raise CommandError('Both directory and DMA pk should be '
                    'provided')
        if not os.path.exists(args[0]):
            raise CommandError('Directory "%s" does not exist'%(
                    args[0],))
        try:
            zone = int(args[1])
        except ValueError:
            raise CommandError('DMA pk "%s" is not an integer number'%(
                    args[1],))
        if not DMA.objects.filter(pk=zone).exists():
            raise CommandError('No DMA exists in db with pk=%s'%(
                    args[1],))
        directory = args[0]
        file_list = [ f for f in listdir(args[0]) if os.path.isfile(
                os.path.join(args[0], f)) and
                f.split('.')[-1].lower()=='csv']
        # TODO: maybe improve transaction control, is this has a
        # meaning, as this command is only for demonstration - concept
        # edition of the iWidget
        with transaction.commit_manually():
            try:
                for file in file_list:
                    process_file(file, directory, zone)
                create_dma_series(zone)
                transaction.commit()
            except:
                transaction.rollback()
                raise

