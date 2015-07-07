__author__ = 'chris'
from django.utils.dateparse import parse_datetime
from django.contrib.auth.models import User
from django import db
from django.db import transaction
import logging
from enhydris.hcore.models import Variable
from enhydris.hcore.models import ReadTimeStep
from iwidget.models import (DMA, Household, IWTimeseries, CUBIC_METERS,
                            TZONE_UTC, VAR_CUMULATIVE, VAR_ENERGY_CUMULATIVE,
                            UNIT_KILOWATTHOUR, VAR_PERIOD,
                            TSTEP_FIFTEEN_MINUTES, TSTEP_DAILY, TSTEP_MONTHLY,
                            TSTEP_HOURLY, VAR_COST, UNIT_EURO,
                            VAR_ENERGY_PERIOD, VAR_ENERGY_COST,
                            GENTITYALTCODETYPE, UserValidationKey,
                            UserNotifications)
from iwidget.cost_calculation \
    import (calculate_cost_timeseries as calculate_cost,
            CUBIC_METER_FLAT_RATE, KWH_FLAT_RATE)
from pthelma.timeseries import Timeseries as TSeries
from pthelma.timeseries import timeseries_bounding_dates_from_db
from pthelma.timeseries import IntervalType
from pthelma.timeseries import read_timeseries_tail_from_db
from math import isnan
from random import randint
from datetime import datetime, timedelta
import numpy as np
from enhydris.settings import SSO_APP
#from profilehooks import timecall

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


def _dif_in_secs(d1, d2):
    """
    This is a helper function, calculating the difference in seconds
    between two timestamps
    """
    return float((d2-d1).days*86400+(d2-d1).seconds)


def create_zone(name):
    """
    We create a hard coded DMA containing the word 'greece'
    """
    zones = DMA.objects.filter(name__icontains=name)[:1]
    if zones:
        return zones[0]
    dma = DMA.objects.create(name=name)
    return dma


def create_dma_series(zone):
    #log.info("*** creating DMA series for zone {x}".format(x=zone))
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
        return User.objects.get(username=identifier), False
    except User.DoesNotExist:
        u = User.objects.create(username=identifier,
                                first_name='Unspecified',
                                last_name='Unspecified',
                                is_staff=False,
                                is_active=True,
                                is_superuser=False,
                                email=identifier+'@example.com')
        pwd = 'iwidgetuser'
        """ in case of the standard householder SSO APP (ie hhApp)
            we create a more complex password. Otherwise we keep the easy one.
        """
        if SSO_APP == "hhApp" and "DEMO" not in identifier:
            u.profile.fname = u.first_name
            u.profile.lname = u.last_name
            u.profile.save()
            # assign random password
            import os
            import binascii
            key = str(binascii.hexlify(os.urandom(4)).upper())
            key = key.replace('E', 'B')
            key = key.replace('0', '1')
            if not key[0].isalpha():
                key = "A" + key[:-1]
            pwd = key
        UserValidationKey\
            .objects.get_or_create(user=u, identifier=m_id, key=pwd)
        u.set_password(pwd)
        u.save()
        return u, True


def create_household(identifier, user, dma_id):
    dma = DMA.objects.get(pk=dma_id)
    try:
        # Change dma if dma is different
        household = Household.objects.get(user=user)
        if household.dma != dma:
            household.dma = dma
            household.save()
            #print "successfully changed DMA to %s" % dma_id
        return household, True
    except Household.DoesNotExist:
        pass
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
    return household, False

#timecall()
def create_raw_timeseries(household):
    db_series = {}
    for variable, unit in [(VAR_CUMULATIVE, CUBIC_METERS),
                           (VAR_ENERGY_CUMULATIVE, UNIT_KILOWATTHOUR)]:
        try:
            series = IWTimeseries.objects.get(gentity=household,
                                              time_step__isnull=True,
                                              variable=variable)
            db_series[{
                VAR_CUMULATIVE: 'WaterCold',
                VAR_ENERGY_CUMULATIVE: 'Electricity'}
                [variable]] = series
            continue
        except IWTimeseries.DoesNotExist:
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

#timecall()
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


#@timecall
def create_objects(data, usernames, force, z_names, z_dict):
    """

    :param data: meter_id -> consumption_type -> [timestamp, volume]
    :param force: True to overwrite
    :return: True for success
    """
    households = []
    # Create user (household owner), household, database series placeholders
    hh_ids = sorted(data.keys())
    found = False
    for hh_id in hh_ids:
        username = usernames[hh_id]
        if username == "PT94993":
            pass
        try:
            zone_name = z_dict[username]
        except KeyError:
            zone_name = z_names[0]
        zone = DMA.objects.get(name=zone_name)
        user, created = create_user(username, hh_id)
        household, found = create_household(hh_id, user, zone.id)
        households.append(household)
        db_series = create_raw_timeseries(household)
        create_processed_timeseries(household)
        timeseries_data = {}
        # Now we will create timeseries.Timeseries() and we will add
        # parsed values
        for variable in db_series:
            if variable not in ('WaterCold', 'Electricity'):
                continue
            exists = False
            s, e = timeseries_bounding_dates_from_db(db.connection,
                                                     db_series[variable].id)
            latest_ts = e
            ts_id = db_series[variable].id
            # checking to see if timeseries records already exist in order
            # to append
            # d = read_timeseries_tail_from_db(db.connection, ts_id)
            total = 0.0
            # if s or e:
            #     exists = True
            #     timeseries = TSeries(ts_id)
            #     timeseries.read_from_db(db.connection)
            # else:
            #     timeseries = TSeries()
            #     timeseries.id = ts_id
            _dict = data[hh_id]
            arr = _dict[variable]
            series = arr
            if not series:
                continue
            earlier = []
            if (not latest_ts) or (latest_ts < series[0][0]):  # append
                timeseries = TSeries()
                timeseries.id = ts_id
                try:
                    tail = read_timeseries_tail_from_db(db.connection, ts_id)
                    total = float(tail[1])  # keep up from last value
                except Exception as e:
                    log.debug(repr(e))
                    total = 0
                for timestamp, value in series:
                    if (not latest_ts) or (timestamp > latest_ts):
                        if not isnan(value):
                            total += value
                            timeseries[timestamp] = total
                        else:
                            timeseries[timestamp] = float('NaN')
                    elif timestamp < latest_ts:
                        earlier.append((timestamp, value))
                timeseries.append_to_db(db=db.connection,
                                        transaction=transaction,
                                        commit=True)
            elif latest_ts >= series[0][0]:
                if not force:  # ignore
                    continue
                else:  # insert
                    for timestamp, value in series:
                        if timestamp < latest_ts:
                            earlier.append((timestamp, value))
            if earlier and ("GR" in username or "GBA" in username):  # insert (only for athens)
                # print "appending %s items for %s" % (len(earlier), username)
                if variable == "WaterCold":
                    ts15 = household \
                        .timeseries.get(time_step__id=TSTEP_FIFTEEN_MINUTES,
                                        variable__id=VAR_PERIOD)
                    series15 = TSeries(id=ts15.id)
                elif variable == "Electricity":
                    ts15 = household \
                        .timeseries.get(time_step__id=TSTEP_FIFTEEN_MINUTES,
                                        variable__id=VAR_ENERGY_PERIOD)
                    series15 = TSeries(id=ts15.id)
                series15.read_from_db(db.connection)
                for ts, value in earlier:
                    series15[ts] = value
                series15.write_to_db(db=db.connection,
                                     transaction=transaction,
                                     commit=True)

                raw_ts = TSeries(ts_id)  # read existing ts raw data
                raw_ts.read_from_db(db.connection)
                total = get_consumption_totals(household, earlier[0][0],
                                               variable)
                init = total
                for timestamp, value in earlier:
                    if not isnan(value):
                        total += value
                        raw_ts[timestamp] = total
                    else:
                        raw_ts[timestamp] = float('NaN')

                # correct later values, too
                diff = total - init
                all_ts = sorted(raw_ts.keys())
                for ts in all_ts:
                    if ts <= timestamp:
                        continue
                    curr = raw_ts[ts]
                    raw_ts[ts] = curr + diff

                raw_ts.write_to_db(db=db.connection,
                                   transaction=transaction,
                                   commit=True)

        if 'WaterCold' in timeseries_data and not found:  # only for new HH
            calc_occupancy(timeseries_data['WaterCold'], household)
    return households


def has_burst(household):
    """
    We won't be using this algorithm any more
    :param household:
    :return:
    """
    name = household.user.username
    if not name.startswith('GR'):
        return 0, 0
    timeseries = household \
        .timeseries.get(time_step__id=TSTEP_FIFTEEN_MINUTES,
                        variable__id=VAR_PERIOD)
    series = TSeries(id=timeseries.id)
    series.read_from_db(db.connection)
    timestamps = sorted(series.keys())
    today = []  # all today's values
    daily_maxes = {}
    for i in range(1, len(timestamps)):
        ts = timestamps[i]
        prev_ts = timestamps[i-1]
        date = ts.date()
        # if previous value is NaN we don't take this value into consideration
        # Because it might have all consumption of all the previous NaN times
        val = series[ts]
        prev_val = series[prev_ts]
        if isnan(prev_val):
            continue
        if i < len(timestamps) - 100:
            if not isnan(val) and not val == 0:
                daily_max = daily_maxes.get(date, 0)
                if val > daily_max:
                    daily_maxes[date] = val
        else:
            tm = "%s-%s-%s %s:%s" % (ts.year, ts.month, ts.day,
                                     ts.time().hour, ts.time().minute)
            if not isnan(val) and not val == 0:
                today.append((val, tm))

    if daily_maxes and today:
        maxes = np.array(daily_maxes.values())
        p = np.percentile(maxes, 90)
        for cons, tm in today:
            if cons > p:
                return cons, tm
    return 0, 0


def get_values_after(household, dt, variable):
    timeseries = None
    if variable == "WaterCold":
        timeseries = household \
            .timeseries.get(time_step__id=TSTEP_FIFTEEN_MINUTES,
                            variable__id=VAR_PERIOD)
    elif variable == "Electricity":
        timeseries = household \
            .timeseries.get(time_step__id=TSTEP_FIFTEEN_MINUTES,
                            variable__id=VAR_ENERGY_PERIOD)
    data = []
    if timeseries:
        series = TSeries(id=timeseries.id)
        series.read_from_db(db.connection)
        timestamps = sorted(series.keys())
        for ts in timestamps:
            val = series[ts]
            if ts <= dt:
                continue
            data.append((ts, val))
    return data


def get_consumption_totals(household, dt, variable):
    """
    Not needed. read_timeseries_tail_from_db does the same thing, faster.
    :param household:
    :return:
    """
    if variable == "WaterCold":
        timeseries = household \
            .timeseries.get(variable__id=VAR_CUMULATIVE)
        raw_series = TSeries(id=timeseries.id)
        raw_series.read_from_db(db.connection)
        timestamps = sorted(raw_series.keys())
        total = 0
        for ts in timestamps:
            val = raw_series[ts]
            if isnan(val):
                continue
            if ts > dt:
                break
            total = raw_series[ts]
        return total
    elif variable == "Electricity":
        timeseries = household \
            .timeseries.get(variable__id=VAR_ENERGY_CUMULATIVE)
        raw_series = TSeries(id=timeseries.id)
        raw_series.read_from_db(db.connection)
        timestamps = sorted(raw_series.keys())
        total = 0
        for ts in timestamps:
            val = raw_series[ts]
            if isnan(val):
                continue
            if ts > dt:
                break
            total = raw_series[ts]
        return total


def has_burst_old(household):
    """
    We won't be using this algorithm any more
    :param household:
    :return:
    """
    name = household.user.username
    if not name.startswith('GR'):
        return 0, 0
    timeseries = household \
        .timeseries.get(time_step__id=TSTEP_FIFTEEN_MINUTES,
                        variable__id=VAR_PERIOD)
    series = TSeries(id=timeseries.id)
    series.read_from_db(db.connection)
    timestamps = sorted(series.keys())
    today = []  # all today's values
    _all = []
    for i in range(1, len(timestamps)):
        ts = timestamps[i]
        if household.user.username == "GR006047" \
                and ts.year == 2015 and ts.month == 2 and ts.day == 9 \
                and ts.hour == 17:
            pass
        prev_ts = timestamps[i-1]
        # if previous value is NaN we don't take this value into consideration
        # Because it might have all consumption of all the previous NaN times
        val = series[ts]
        prev_val = series[prev_ts]
        if isnan(prev_val):
            continue
        if i < len(timestamps) - 100:
            if not isnan(val) and not val == 0:
                _all.append(series[ts])
        else:
            tm = "%s:%s" % (ts.time().hour, ts.time().minute)
            if not isnan(val) and not val == 0:
                today.append((val, tm))

    if _all and today:
        all1 = np.array(_all)
        p = np.percentile(all1, 95)
        for cons, tm in today:
            if cons > p:
                return cons, tm
    return 0, 0


def has_leakage(household):
    """
    This method checks for leakages. The way it is done is pretty simple
     I open the hourly timeseries and retrieve all timestamps.
     I create a dictionary with keys be the dates (not time) and values arrays
     be the percentage of night/total consumption
    :param household:
    :return: False for no leakage, True for leakage
    """
    name = household.user.username
    if name == "GR059E35":
        pass
    if name.startswith('GB'):  # not UK because they send daily data
        return 0, 0
    timeseries = household \
        .timeseries.get(time_step__id=TSTEP_HOURLY,
                        variable__id=VAR_PERIOD)
    series = TSeries(id=timeseries.id)
    series.read_from_db(db.connection)
    timestamps = sorted(series.keys())
    night_dict = {}
    total_dict = {}
    _t = datetime.now().time()
    _d = datetime.today().date()
    for ts in timestamps:
        _d = ts.date()
        _t = ts.time()
        val = series[ts]
        if 3 <= _t.hour <= 5:
            if val == 0:
                night_dict[_d] = 0  # make all night 0 if one 0
            else:
                try:
                    night_dict[_d] += val
                except KeyError:
                    night_dict[_d] = val
        try:
            total_dict[_d] += val
        except KeyError:
            total_dict[_d] = val

    #remove last day if not a whole day (_t < 24:00)
    if _t.hour < 23:
        try:
            del total_dict[_d]
            del night_dict[_d]
        except (KeyError, IndexError):
            pass
    _all = []  # all lengths will be in here
    _today = []  # today's lengths

    _dates = sorted(total_dict.keys())[:-1]  # all except last day 4 * 15min for 4 hrs
    for _d in _dates:
        total = total_dict[_d]
        # there can be a case when I don't get data for 01:00 -> 04:00
        # so night[_d] might not exist. in this case let it be zero
        try:
            night = night_dict[_d]
        except KeyError:
            night = 0
        if total > 0 and night > 0 and not isnan(total) and not isnan(night):
            _all.append(float(night) / float(total))

    # Now we need only the last day. However sometimes we have
    # some timestamps from the next day because the file has all data from
    # previous day and one entry from today. So we pick today and yesterday
    # instead of today. Today is too small. And too fast some times. But that
    # is for some other time to discuss...
    _dates = sorted(total_dict.keys())[-1:]  # only last day's
    for _d in _dates:
        total = total_dict[_d]
        night = night_dict[_d]
        if total > 0 and night > 0 and not isnan(total) and not isnan(night):
            _today.append(float(night) / float(total))
    if _all and _today:
        ts = timestamps[-1]
        tm = "%s-%s-%s %s:%s" % (ts.year, ts.month, ts.day,
                                 ts.time().hour, ts.time().minute)
        all1 = np.array(_all)
        p = np.percentile(all1, 90)
        for val in _today:
            if val > p:
                return val, tm
    return 0, 0


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

#@timecall()
def regularize(raw_series_db, proc_series_db, rs, re):
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
    try:
        test_value = raw_series[raw_series.bounding_dates()[1]]
    except Exception as e:
        #log.debug("Trying to get test value for raw series %s failed with %s. "
        #          "Skipping!" % (raw_series_db.id, repr(e)))
        return None
    time_step = ReadTimeStep(proc_series_db.id, proc_series_db)
    proc_series = TSeries(id=proc_series_db.id, time_step=time_step)
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
    while pointer <= end:
        proc_series[pointer] = float('nan')
        pointer = proc_series.time_step.next(pointer)
    # Pass 2: Transfer cummulative raw series to differences series:
    prev_s = 0
    for i in xrange(len(raw_series)):
        dat, value = raw_series.items(pos=i)
        d = datetime.today()
        d = d.replace(month=11).replace(day=5)
        if dat.date() == d.date():
            pass
        if not isnan(value):
            # "if" Added by Chris Pantazis, because sometimes
            # We get a negative small value by the meter
            if prev_s > value:
                prev_s = value
            raw_series[dat] = value-prev_s
            prev_s = value
    # Pass 3: Regularize step: loop over raw series records and distribute
    # floating point values to processed series
    for i in xrange(len(raw_series)):
        dat, value = raw_series.items(pos=i)
        if not isnan(value):
            # find previous, next timestamp of the proc time series
            d1 = proc_series.time_step.down(dat)
            d2 = proc_series.time_step.up(dat)
            if isnan(proc_series[d1]):
                proc_series[d1] = 0
            if isnan(proc_series[d2]):
                proc_series[d2] = 0
            if d1 == d2:  # if dat on proc step then d1=d2
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
    # log.info("%s = %s = %s ?" % (raw_series.sum(),
    # proc_series.sum(), test_value))

    proc_series.write_to_db(db=db.connection, commit=True)
    #return the full timeseries
    return proc_series

#@timecall()
def aggregate(household, source_time_series, dest_timestep_id, variable):
    MISSING_ALLOWED = {
        TSTEP_HOURLY: 4,
        TSTEP_DAILY: 20,
        TSTEP_MONTHLY: 30
    }
    BOUNDS = {
        TSTEP_HOURLY: ('hourly_start', 'hourly_end'),
        TSTEP_DAILY: ('daily_start', 'daily_end'),
        TSTEP_MONTHLY: ('monthly_start', 'monthly_end')
    }
    dest_timeseries_db = household.\
        timeseries.get(time_step__id=dest_timestep_id, variable__id=variable)
    dest_time_step = ReadTimeStep(dest_timeseries_db.id,
                                  dest_timeseries_db)
    if not source_time_series.bounding_dates():
        return
    #
    # PROBLEM: When I give hourly I can't get daily destination timeseries!!
    dest_timeseries = source_time_series.aggregate(
        target_step=dest_time_step,
        missing_allowed=MISSING_ALLOWED[dest_timestep_id],
        missing_flag='MISSING')[0]
    dest_timeseries.id = dest_timeseries_db.id
    dest_timeseries.write_to_db(db=db.connection, commit=True)
    for i, func in ((0, min), (1, max)):
        if not dest_timeseries.bounding_dates():
            break
        bounds[variable][BOUNDS[dest_timestep_id][i]] = func(
            bounds[variable][BOUNDS[dest_timestep_id][i]],
            dest_timeseries.bounding_dates()[i])
    return dest_timeseries


#@timecall()
def process_household(household):
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
        #log.info("Now regularizing %s with id %s for s1=%s and e1=%s"
        #         % (raw_series_db, raw_series_db.id, s1, e1))
        fifteen_min_series = regularize(raw_series_db, fifteen_min_series_db,
                                        s1, e1)
        if fifteen_min_series and fifteen_min_series.bounding_dates():
            bounds[variable]['fifteen_start'] = min(
                bounds[variable]['fifteen_start'],
                fifteen_min_series.bounding_dates()[0])
            bounds[variable]['fifteen_end'] = max(
                bounds[variable]['fifteen_end'],
                fifteen_min_series.bounding_dates()[1])

            result = fifteen_min_series
            monthly_series = None
            # Stefanos wants to aggregate using previous results
            # Why? The problem is that Monthly series is not inserted.
            # Was this on purpose?
            for time_step_id in (TSTEP_HOURLY, TSTEP_DAILY, TSTEP_MONTHLY):
                result = aggregate(household, result, time_step_id, variable)
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
                log.info("Error in monthly calculation %s. Skipping!" % repr(e))
                continue


@transaction.commit_manually
def process_data(data, usernames, force, z_names, zone_dict):
    """
    this means to be a common ground for all csv importers. Remember that we
    need the date to be in the format yyyy-mm-dd.
    :param data: dictionary of dictionaries of lists
    { meter_id -> consumption_type -> [timestamp, volume] }
    :param usernames: dictionary of usernames for the meter_ids
    :param force: True to rewrite
    :param zone_dict: dictionary to hold zone for each username. Important for
    cases when there are multiple zones
    :return: Error (0: if none)
    """
    dma = None
    try:
        global log
        for name in z_names:
            dma = create_zone(name)
            create_dma_series(dma.id)  # this might not be needed, actually
        # dma = DMA.objects.get(pk=dma.id)
        households = create_objects(data, usernames, force, z_names, zone_dict)
        for household in households:
            log.debug("processing household %s" % household.user.username)
            try:
                process_household(household)
                log.debug("done")
            except Exception as e:
                log.debug("error %s" % repr(e))
            cons, _time = has_leakage(household)
            if cons:
                today = datetime.today()
                yesterday = today - timedelta(days=1)
                UserNotifications.objects.get_or_create(user=household.user,
                                                        notification="leakage",
                                                        detected=yesterday,
                                                        consumption=cons * 1000,
                                                        event_time=_time)
            cons, _time = has_burst(household)
            if cons:
                today = datetime.today()
                yesterday = today - timedelta(days=1)
                UserNotifications.objects.get_or_create(user=household.user,
                                                        notification="burst",
                                                        detected=yesterday,
                                                        consumption=cons * 1000,
                                                        event_time=_time)
        log.info("Process ended... Committing!")
        transaction.commit()
        log.info("SUCCESS!")
    except Exception as e:
        log = logging.getLogger(__name__)
        log.debug("Transaction failed because %s. Rolling back!" % repr(e))
        transaction.rollback()
