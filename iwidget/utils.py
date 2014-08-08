# -*- coding: utf-8 -*- #!/usr/bin/python

# iWidget application for openmeteo Enhydris software
# This software is provided with the AGPL license
# Copyright (c) 2013-2014 National Techincal University of Athens

from datetime import datetime, timedelta
import math

from django.core.cache import cache
from django.db import connection

from pthelma.timeseries import Timeseries

from enhydris.hcore.models import ReadTimeStep

from .cost_calculation import (monthly_cost_from_consumption,
    KWH_FLAT_RATE)

# Target consumption in cubic meters per capita per day
TARGET_CONSUMPTION = 0.120

def _load_daily_series_data(ts_daily):
    time_step = ReadTimeStep(ts_daily.id, ts_daily)
    timeseries = Timeseries(time_step=time_step,
            id=ts_daily.id)
    timeseries.read_from_db(connection)
    return timeseries

def aggregate_period(timeseries, start, end):
    bounding_dates = timeseries.bounding_dates()
    start = timeseries.time_step.up(start)
    end = timeseries.time_step.down(end)
    if any((not bounding_dates, end<start)):
        return 0
    position = start
    result = 0
    while position<=end:
        if position not in timeseries:
            position = timeseries.time_step.next(position)
            continue
        value = timeseries[position]
        if math.isnan(value):
            position = timeseries.time_step.next(position)
            continue
        result += value
        position = timeseries.time_step.next(position)
    return result

def _dec_year(timestamp):
    return timestamp.replace(year=timestamp.year-1)

def statistics_on_daily(ts_daily, occupancy = 1):
    cache_key = 'daily_statistics__%d'%(ts_daily.id,)
    cache_value = cache.get(cache_key)
    if cache_value is not None:
        return cache_value
    timeseries = _load_daily_series_data(ts_daily)
    bounding_dates = timeseries.bounding_dates()
    if not bounding_dates:
        cache.set(cache_key, None, 600)
        return
    result = {}
    today = bounding_dates[1]
    result['today_timestamp'] = today
    result['today'] = timeseries[today]*1000.0
    if math.isnan(result['today']): result['today'] = 0.0
    result['today_last_year'] = timeseries.get(
        _dec_year(today), 0)*1000.0
    if math.isnan(result['today_last_year']):
        result['today_last_year'] = 0.0
    last_7_days_timestamp = today-timedelta(days=6)
    result['last_7_days_timestamp'] = last_7_days_timestamp
    result['last_7_days'] = aggregate_period(
        timeseries,
        last_7_days_timestamp,
        today)*1000.0

    """
        ADDED YESTERDAY's CONSUMPTION VALUE BY CHRIS PANTAZIS
    """
    result['yesterday'] = timeseries[today-timedelta(days=1)]*1000.0
    """
        ADDED CURRENT WEEK CONSUMPTION VALUE BY CHRIS PANTAZIS
    """
    result['current_week'] = aggregate_period(
        timeseries,
        today-timedelta(days=today.weekday()),
        today)*1000.0
    """
        ADDED LAST WEEK CONSUMPTION VALUE BY CHRIS PANTAZIS
    """
    result['last_week'] = aggregate_period(
        timeseries,
        today-timedelta(days=today.weekday()+7),
        today-timedelta(days=today.weekday()+1))*1000.0
    """
        ADDED CURRENT WEEK LAST YEAR CONSUMPTION VALUE BY CHRIS PANTAZIS
    """
    result['current_week_last_year'] = aggregate_period(
        timeseries,
        _dec_year(today-timedelta(days=today.weekday())),
        _dec_year(today))*1000.0
    """
        ADDED LAST MONTH CONSUMPTION VALUE BY CHRIS PANTAZIS
    """
    last_day_of_last_month = today.replace(day=1) - timedelta(days=1)
    first_day_of_last_month = last_day_of_last_month.replace(day=1)
    result['last_month'] = aggregate_period(
        timeseries, first_day_of_last_month, last_day_of_last_month)*1000.0
    """
        CODE ADDED BY CHRIS PANTAZIS ENDS HERE
    """
    result['last_7_days_last_year'] = aggregate_period(
        timeseries,
        _dec_year(today-timedelta(days=6)),
        _dec_year(today))*1000.0
    result['current_month'] = aggregate_period(
        timeseries,
        today.replace(day=1),
        today)
    result['current_month_last_year'] = aggregate_period(
        timeseries,
        _dec_year(today.replace(day=1)),
        _dec_year(today))
    result['current_year'] = aggregate_period(
        timeseries,
        today.replace(day=1, month=1),
        today)
    result['last_year'] = aggregate_period(
        timeseries,
        _dec_year(today.replace(day=1, month=1)),
        _dec_year(today))
    result['last_7_days_cost'] = monthly_cost_from_consumption(
        result['last_7_days']*0.001)
    result['last_7_days_last_year_cost'] = monthly_cost_from_consumption(
        result['last_7_days_last_year']*0.001)
    result['current_month_cost'] = monthly_cost_from_consumption(
        result['current_month'])
    result['current_month_last_year_cost'] = monthly_cost_from_consumption(
        result['current_month_last_year'])
    result['current_year_cost'] = monthly_cost_from_consumption(
        result['current_year'])
    result['last_year_cost'] = monthly_cost_from_consumption(
        result['last_year'])
    daily_consumption = occupancy * TARGET_CONSUMPTION
    result['target_daily'] = daily_consumption * 1000.0
    result['target_weekly'] = daily_consumption * 7.0 * 1000.0
    result['target_month'] = daily_consumption * today.day
    result['target_year'] = daily_consumption * ((today - 
            today.replace(month=1, day=1)).days + 1)
    """
        CODE ADDED BY CHRIS PANTAZIS at 07/08/2014
        NEXT FRAGMENT ADDS DICTIONARY ENTRIES FOR TARGET
        CONSUMPTION (Lit/Person/Day) AND DECIDES HOW GOOD IT WAS
        FOR EXAMPLE IF CONSUMPTION IS LESS THAN 80 lt/p/d THEN NO OF SMILES
        WILL BE 5:
        result['current_day_target'] = ['1', '2', '3', '4', '5']
        SO WE CAN DO A FOR-LOOP IN THE TEMPLATE TO SHOW len() SMILES
        (IF array is empty then show sad face, instead!)
    """
    result['today_lpd'] = get_lpd_arr(result['today'], occupancy, 'day', today)
    result['current_week_lpd'] = get_lpd_arr(result['current_week'],
                                             occupancy, 'day', today)
    result['current_month_lpd'] = get_lpd_arr(result['current_month'],
                                              occupancy, 'day', today)
    result['current_year_lpd'] = get_lpd_arr(result['current_year'],
                                             occupancy, 'day', today)
    """
        CHRIS PANTAZIS CODE ENDS HERE
    """
    cache.set(cache_key, result, 600)
    return result


def get_lpd_arr(val, occupants, period, today):
    """
    Author: Chris Pantazis (07/08/2014)
    This function returns an array of literals depending on
    the target consumption per person per day for the current household.
    This is actually a workaround.
    Needed in <<summary.html>> template file to print correct number of smilies

    :param val: Total consumption for period (float)
    :param occupants: Number of occupants (int)
    :param period: day, week, month, year (string)
    :param today: today's date. (Divide by weekday instead of 7 for example)
    :return: array that has a len of 5,4,3,2,1 or 0 for number of smilies
    """
    lpd = 0
    #first find current period
    if period == 'day':
        lpd = val / occupants
    elif period == 'week':
        lpd = val / (today.weekday() + 1) / occupants
    elif period == 'month':
        lpd = val / today.day / occupants
    elif period == 'year':
        lpd = val / today.timetuple().tmyday / occupants

    if lpd <= 80:
        return [1, 2, 3, 4, 5]
    elif lpd <= 90:
        return [1, 2, 3, 4]
    elif lpd <= 105:
        return [1, 2, 3]
    elif lpd <= 110:
        return [1, 2]
    elif lpd <= 120:
        return [1]
    elif lpd <= 150:
        return []



# Target consumption in kWh per capita per day
TARGET_ENERGY_CONSUMPTION = 5.0

def energy_statistics_on_daily(ts_daily, occupancy = 1):
    cache_key = 'daily_energy_statistics__%d'%(ts_daily.id,)
    cache_value = cache.get(cache_key)
    if cache_value is not None:
        return cache_value
    timeseries = _load_daily_series_data(ts_daily)
    bounding_dates = timeseries.bounding_dates()
    if not bounding_dates:
        cache.set(cache_key, None, 600)
        return
    result = {}
    today = bounding_dates[1]
    result['today_timestamp'] = today
    result['today'] = timeseries[today]
    if math.isnan(result['today']): result['today'] = 0.0
    result['today_last_year'] = timeseries.get(
            _dec_year(today), 0)
    if math.isnan(result['today_last_year']):
        result['today_last_year'] = 0.0
    last_7_days_timestamp = today-timedelta(days=6)
    result['last_7_days_timestamp'] = last_7_days_timestamp
    result['last_7_days'] = aggregate_period(
            timeseries,
            last_7_days_timestamp,
            today)
    result['last_7_days_last_year'] = aggregate_period(
            timeseries,
            _dec_year(today-timedelta(days=6)),
            _dec_year(today))
    result['current_month'] = aggregate_period(
            timeseries,
            today.replace(day=1),
            today)
    result['current_month_last_year'] = aggregate_period(
            timeseries,
            _dec_year(today.replace(day=1)),
            _dec_year(today))
    result['current_year'] = aggregate_period(
            timeseries,
            today.replace(day=1, month=1),
            today)
    result['last_year'] = aggregate_period(
            timeseries,
            _dec_year(today.replace(day=1, month=1)),
            _dec_year(today))
    result['last_7_days_cost'] = monthly_cost_from_consumption(
            result['last_7_days'], rate=KWH_FLAT_RATE)
    result['last_7_days_last_year_cost'] = monthly_cost_from_consumption(
            result['last_7_days_last_year'], rate=KWH_FLAT_RATE)
    result['current_month_cost'] = monthly_cost_from_consumption(
            result['current_month'], rate=KWH_FLAT_RATE)
    result['current_month_last_year_cost'] = monthly_cost_from_consumption(
            result['current_month_last_year'], rate=KWH_FLAT_RATE)
    result['current_year_cost'] = monthly_cost_from_consumption(
            result['current_year'], rate=KWH_FLAT_RATE)
    result['last_year_cost'] = monthly_cost_from_consumption(
            result['last_year'], rate=KWH_FLAT_RATE)
    daily_consumption = occupancy * TARGET_ENERGY_CONSUMPTION
    result['target_daily'] = daily_consumption
    result['target_weekly'] = daily_consumption * 7.0
    result['target_month'] = daily_consumption * today.day
    result['target_year'] = daily_consumption * ((today - 
            today.replace(month=1, day=1)).days + 1)
    cache.set(cache_key, result, 600)
    return result

