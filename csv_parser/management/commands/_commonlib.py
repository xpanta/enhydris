__author__ = 'chris'
from django.utils.dateparse import parse_datetime
from django.contrib.auth.models import User
from django import db
from django.db import transaction
import logging
from enhydris.hcore.models import Variable
from iwidget.models import (DMA, Household, IWTimeseries, CUBIC_METERS,
                            TZONE_UTC, VAR_CUMULATIVE, VAR_ENERGY_CUMULATIVE,
                            UNIT_KILOWATTHOUR, VAR_PERIOD,
                            TSTEP_FIFTEEN_MINUTES, TSTEP_DAILY, TSTEP_MONTHLY,
                            TSTEP_HOURLY, VAR_COST, UNIT_EURO,
                            VAR_ENERGY_PERIOD, VAR_ENERGY_COST,
                            GENTITYALTCODETYPE, UserValidationKey)
from iwidget.cost_calculation \
    import (calculate_cost_timeseries as calculate_cost,
            CUBIC_METER_FLAT_RATE, KWH_FLAT_RATE)
from pthelma.timeseries import Timeseries as TSeries
from pthelma.timeseries import timeseries_bounding_dates_from_db
from pthelma.timeseries import IntervalType
from pthelma.timeseries import read_timeseries_tail_from_db
from math import isnan
from random import randint
from datetime import datetime

AVERAGE_UNIT_WATER_CONSUMPTION = 100.000
log = logging.getLogger(__name__)

MAX_DATE = datetime(2100, 1, 1, 0, 0, 0)
MIN_DATE = datetime(1900, 1, 1, 0, 0, 0)

bounds = {
    VAR_PERIOD: {
        'fifteen_start': MAX_DATE, 'fifteen_end': MIN_DATE,
        'hourly_start': MAX_DATE, 'hourly_end': MIN_DATE,
        'daily_start': MAX_DATE, 'daily_end': MIN_DATE,
        'monthly_start': MAX_DATE, 'monthly_end': MIN_DATE},
    VAR_ENERGY_PERIOD: {
        'fifteen_start': MAX_DATE, 'fifteen_end': MIN_DATE,
        'hourly_start': MAX_DATE, 'hourly_end': MIN_DATE,
        'daily_start': MAX_DATE, 'daily_end': MIN_DATE,
        'monthly_start': MAX_DATE, 'monthly_end': MIN_DATE}
}


def create_zone(name):
    """
    We create a hard coded DMA containing the word 'greece'
    """
    zones = DMA.objects.filter(name__icontains='greece')[:1]
    if zones:
        return zones[0]
    dma = DMA.objects.create(name=name)
    return dma


def create_dma_series(zone):
    log.info("*** creating DMA series for zone {x}".format(x=zone))
    # nominal_offset_minutes, months, actual_offset_minutes, months
    # name, variable, unit
    tseries_list = {
        (TSTEP_HOURLY, VAR_PERIOD): [0, 0, 0, 0, 'Hourly consumption',
                                     VAR_PERIOD, CUBIC_METERS],
        (TSTEP_DAILY, VAR_PERIOD): [0, 0, 1440, 0, 'Daily consumption',
                                    VAR_PERIOD, CUBIC_METERS],
        (TSTEP_MONTHLY, VAR_PERIOD): [0, 0, 0, 1, 'Monthly consumption',
                                      VAR_PERIOD, CUBIC_METERS],
        (TSTEP_HOURLY, VAR_ENERGY_PERIOD): [0, 0, 0, 0, 'Hourly energy',
                                            VAR_ENERGY_PERIOD,
                                            UNIT_KILOWATTHOUR],
        (TSTEP_DAILY, VAR_ENERGY_PERIOD): [0, 0, 1440, 0, 'Daily energy',
                                           VAR_ENERGY_PERIOD,
                                           UNIT_KILOWATTHOUR],
        (TSTEP_MONTHLY, VAR_ENERGY_PERIOD): [0, 0, 0, 1, 'Monthly energy',
                                             VAR_ENERGY_PERIOD,
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
                name += ' - per capita'
                exists_qs = exists_qs.filter(name__icontains='capita')
            if exists_qs.exists():
                continue
            skipped = False
            variable = tseries_list[ts][5]
            unit = tseries_list[ts][6]
            ts_object = IWTimeseries.objects.create(
                time_step_id=time_step_id,
                gentity_id=zone,
                variable_id=variable,
                interval_type_id=IntervalType.SUM,
                time_zone_id=TZONE_UTC,
                unit_of_measurement_id=unit,
                name=name,
                nominal_offset_minutes=tseries_list[ts][0],
                nominal_offset_months=tseries_list[ts][1],
                actual_offset_minutes=tseries_list[ts][2],
                actual_offset_months=tseries_list[ts][3],
            )
            assert ts_object
    if skipped:
        log.debug("Series for zone {x} exists. Skipping".format(x=zone))


def create_user(identifier, m_id):
    """Identifier will be used as username == household name"""
    try:
        return User.objects.get(username=identifier)
    except User.DoesNotExist:
        u = User.objects.create(username=identifier,
                                first_name='Unspecified',
                                last_name='Unspecified',
                                is_staff=False,
                                is_active=True,
                                is_superuser=False,
                                email=identifier+'@example.com')
        u.set_password('iwidgetuser')
        u.save()
        u.profile.fname = u.first_name
        u.profile.lname = u.last_name
        u.profile.save()
        # assign random validation key
        import os
        import binascii
        key = binascii.hexlify(os.urandom(5))
        UserValidationKey\
            .objects.get_or_create(user=u, identifier=m_id, key=key)
        return u


def create_household(identifier, user, dma_id):
    try:
        return Household.objects.get(user=user)
    except Household.DoesNotExist:
        pass
    # DMA (it is 1) should be one created at the start. But we removed DMAs
    # so I hardcoded 1 because creating DMA and Household objects both
    # create entries in the Gentity model for no reason (this is why
    # model inheritance is a bitch and we should avoid it.
    dma = DMA.objects.get(pk=dma_id)
    household = Household.objects.create(
        user=user,
        dma=dma,
        property_type_id=1,
        num_of_occupants=randint(1, 5),
        address='Unknown')
    # We also create an "alternative" id entry based on the given
    # identifier, for future use
    household.alt_codes.create(type_id=GENTITYALTCODETYPE,
                               value=identifier.lstrip('0'))
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
        var = Variable.objects.get(pk=variable)
        name = var.descr
        # used to be "create" but I changed it to get_or_create
        # so as not to create duplicate items.
        series, created = IWTimeseries.objects.get_or_create(
            gentity=household,
            variable_id=variable,
            time_zone_id=TZONE_UTC,
            unit_of_measurement_id=unit,
            name=name,
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
        (TSTEP_FIFTEEN_MINUTES, 0, 0, 0, 0, 'Fifteen minutes consumption',
         VAR_PERIOD),
        (TSTEP_HOURLY, 0, 0, 0, 0, 'Hourly consumption', VAR_PERIOD),
        (TSTEP_DAILY, 0, 0, 1440, 0, 'Daily consumption', VAR_PERIOD),
        (TSTEP_MONTHLY, 0, 0, 0, 1, 'Monthly consumption', VAR_PERIOD),
        (TSTEP_FIFTEEN_MINUTES, 0, 0, 0, 0,
         'Fifteen minutes energy consumption', VAR_ENERGY_PERIOD),
        (TSTEP_HOURLY, 0, 0, 0, 0, 'Hourly energy consumption',
         VAR_ENERGY_PERIOD),
        (TSTEP_DAILY, 0, 0, 1440, 0, 'Daily energy consumption',
         VAR_ENERGY_PERIOD),
        (TSTEP_MONTHLY, 0, 0, 0, 1, 'Monthly energy consumption',
         VAR_ENERGY_PERIOD),
        (TSTEP_MONTHLY, 0, 0, 0, 1, 'Monthly cost', VAR_COST),
        (TSTEP_MONTHLY, 0, 0, 0, 1, 'Monthly energy cost', VAR_ENERGY_COST),
    ]
    for ts in tseries_list:
        variable_id = ts[6]
        time_step_id = ts[0]
        ddd = {
            VAR_COST: UNIT_EURO,
            VAR_ENERGY_COST: UNIT_EURO,
            VAR_PERIOD: CUBIC_METERS,
            VAR_ENERGY_PERIOD: UNIT_KILOWATTHOUR}
        unit_of_measurement_id = ddd[variable_id]
        if IWTimeseries.objects.filter(gentity=household,
                                       time_step__id=time_step_id,
                                       variable__id=variable_id).exists():
            continue
        ts_object, created = IWTimeseries.objects.get_or_create(
            time_step_id=time_step_id,
            gentity=household,
            variable_id=variable_id,
            interval_type_id=IntervalType.SUM,
            time_zone_id=TZONE_UTC,
            unit_of_measurement_id=unit_of_measurement_id,
            name=ts[5],
            nominal_offset_minutes=ts[1],
            nominal_offset_months=ts[2],
            actual_offset_minutes=ts[3],
            actual_offset_months=ts[4],
        )
        assert ts_object


def create_objects(data, usernames, force, zone):
    """

    :param dma: the DMA the household belongs
    :param data: meter_id -> consumption_type -> [timestamp, volume]
    :param force: True to overwritte
    :return: True for success
    """
    households = []
    log.debug("processing household data now...")
    # Create user (household owner), household, database series placeholders
    hh_ids = data.keys()
    for hh_id in hh_ids:
        username = usernames[hh_id]
        user = create_user(username, hh_id)
        log.info("*** created user %s ***" % user)
        household = create_household(hh_id, user, zone.id)
        log.info("*** created household %s ***" % hh_id)
        db_series = create_raw_timeseries(household)
        log.info("*** created raw timeseries ***")
        create_processed_timeseries(household)
        log.info("*** created processed timeseries ***")
        timeseries_data = {}
        # Now we will create timeseries.Timeseries() and we will add
        # parsed values
        for variable in db_series:
            if variable not in ('WaterCold', 'Electricity'):
                continue
            s, e = timeseries_bounding_dates_from_db(db.connection,
                                                     db_series[variable].id)
            if not force and (s or e):
                log.debug('Raw timeseries id=%s has data, '
                          'skipping.' % db_series[variable].id)
                continue
            ts_id = db_series[variable].id
            # checking to see if timeseries records already exist in order
            # to append
            d = read_timeseries_tail_from_db(db.connection, ts_id)
            exists = False
            if not d:
                timeseries = TSeries()
            else:
                timeseries = TSeries(ts_id)
                exists = True

            timeseries.id = ts_id
            households.append(household)
            total = 0.0
            _dict = data[hh_id]
            arr = _dict[variable]
            series = arr
            for timestamp, value in series:
                if not isnan(value):
                    total += value
                    timeseries[timestamp] = total
                else:
                    timeseries[timestamp] = float('NaN')
            timeseries_data[variable] = timeseries
            log.info("*** writing timeseries data to db")
            if not exists:
                timeseries.write_to_db(db=db.connection,
                                       transaction=transaction,
                                       commit=False)
            else:
                timeseries.append_to_db(db=db.connection,
                                        transaction=transaction,
                                        commit=False)
        if 'WaterCold' in timeseries_data:
            calc_occupancy(timeseries_data['WaterCold'], household)
    return households

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
    while i < count:
        timestamp, value = timeseries.items(pos=i)
        if not isnan(value) and value > 0.0:
            first_record = timestamp, value
            break
        i += 1
    i = count-1
    while i >= 0:
        timestamp, value = timeseries.items(pos=i)
        if not isnan(value):
            last_record = timestamp, value
            break
        i -= 1
    if first_record and last_record:
        diff = float((last_record[0]-first_record[0]).days)
        average_consumption = last_record[1]*1000.0 / (diff + 0.1)  # for diff=0
        num_of_occupants = max(1,
                               int(round(
                                   average_consumption /
                                   AVERAGE_UNIT_WATER_CONSUMPTION)))
        household.num_of_occupants = num_of_occupants
        household.save()


def regularize():
    pass


def aggregate():
    pass


def process_household(household):
    print "Processing household: %s" % (household.alt_codes.all()[0],)
    for variable in (VAR_PERIOD, VAR_ENERGY_PERIOD):
        raw_series_db = household \
            .timeseries \
            .filter(time_step__isnull=True,
                    variable__id={
                        VAR_PERIOD: VAR_CUMULATIVE,
                        VAR_ENERGY_PERIOD: VAR_ENERGY_CUMULATIVE
                    }[variable])[:1]
        if not raw_series_db:
            continue
        raw_series_db = raw_series_db[0]
        fifteen_min_series_db = household \
            .timeseries.get(time_step__id=TSTEP_FIFTEEN_MINUTES,
                            variable__id=variable)
        s1, e1 = timeseries_bounding_dates_from_db(db.connection,
                                                   raw_series_db.id)
        s2, e2 = timeseries_bounding_dates_from_db(db.connection,
                                                   fifteen_min_series_db.id)
        #    if e2 and (e1-e2).seconds<15*60:
        #        return
        fifteen_min_series = regularize(raw_series_db, fifteen_min_series_db, s1,e1,s2,e2)
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
            result = aggregate(bounds, household, result, time_step_id, variable)
            if time_step_id == TSTEP_MONTHLY:
                monthly_series = result
        if not monthly_series:
            return
        # Cost calculation only if monthly_series present
        try:
            cost_timeseries_db = household \
                .timeseries.get(time_step__id=TSTEP_MONTHLY,
                                variable__id={
                                    VAR_PERIOD: VAR_COST,
                                    VAR_ENERGY_PERIOD: VAR_ENERGY_COST
                                }[variable])
            cost_timeseries = calculate_cost(monthly_series,
                                             rate={
                                                 VAR_PERIOD: CUBIC_METER_FLAT_RATE,
                                                 VAR_ENERGY_PERIOD: KWH_FLAT_RATE
                                             }[variable])
            cost_timeseries.id = cost_timeseries_db.id
            cost_timeseries.write_to_db(db=db.connection, commit=True)
        except Exception as e:
            print repr(e)
            print "error in monthly cost calculation. Skipping"
            continue



@transaction.commit_manually
def process_data(data, usernames, force, name):
    """
    this means to be a common ground for all csv importers. Remember that we
    need the date to be in the format yyyy-mm-dd.
    :param data: dictionary of dictionaries of lists
    { meter_id -> consumption_type -> [timestamp, volume] }
    :param usernames: dictionary of usernames for the meter_ids
    :param force: True to rewrite
    :return: Error (0: if none)
    """
    dma = None
    try:
        global log
        log.info("Processing data...")
        dma = create_zone(name)
        log.info("*** Created DMA {x} with id {y}".format(x=dma.name, y=dma.id))
        #create_dma_series(dma.id)  # this might not be needed, actually
        #dma = DMA.objects.get(pk=dma.id)
        households = create_objects(data, usernames, force, dma)
        for household in households:
            log.info("Processing ts records for household %s" % household)
            process_household(household, bounds)
        log.info("Process ended... Committing!")
        #transaction.commit()
        log.info("SUCCESS!")
    except Exception as e:
        log = logging.getLogger(__name__)
        log.debug("Transaction failed while entering data for zone {x}"
                  " because of error {y}". format(x=dma.id, y=repr(e)))
        transaction.rollback()
