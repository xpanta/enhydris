# -*- coding: utf-8 -*- #!/usr/bin/python

# iWidget application for openmeteo Enhydris software
# This software is provided with the AGPL license
# Copyright (c) 2013-2014 National Techincal University of Athens

from datetime import datetime, timedelta
import math
# ADDED By Chris Pantazis to find month's maximum target value
from calendar import monthrange
#
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
    """
    Note: multiplying timeseries by 1000.0 becomes litres. Otherwise it is
    cubic metres
    :param ts_daily:
    :param occupancy:
    :return:
    """
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
    try:
        result['yesterday'] = timeseries[today-timedelta(days=1)]*1000.0
    except KeyError:
        result['yesterday'] = 0
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
    try:
        vv = aggregate_period(
            timeseries,
            today-timedelta(days=today.weekday()+7),
            today-timedelta(days=today.weekday()+1))*1000.0
        result['last_week'] = vv
    except KeyError:
        result['last_week'] = 0
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
        today) * 1000.0
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
        CODE ADDED BY Chris Pantazis at 07/08/2014
        NEXT FRAGMENT ADDS DICTIONARY ENTRIES FOR TARGET
        CONSUMPTION (Lit/Person/Day) AND DECIDES HOW GOOD IT WAS
        FOR EXAMPLE IF CONSUMPTION IS LESS THAN 80 lt/p/d THEN NO OF SMILES
        WILL BE 5:
        result['current_day_target'] = ['1', '2', '3', '4', '5']
        SO WE CAN DO A FOR-LOOP IN THE TEMPLATE TO SHOW len() SMILES
        (IF array is empty then show sad face, instead!)
    """
    targets = [80, 90, 105, 110, 120]
    daily_max = []
    weekly_max = []
    monthly_max = []
    yearly_max = []
    cc = monthrange(today.year, today.month)
    for t in targets:
        daily_max.append(t * occupancy)
        weekly_max.append(t * 7 * occupancy)
        monthly_max.append(t * int(cc[1]) * 80 * occupancy)
        yearly_max.append(t * 365 * occupancy)

    cdc = result["today"]
    cwc = result["current_week"]
    cmc = result["current_month"]
    cyc = result["current_year"]

    ctd = result['current_target_day'] = get_next_target(cdc, daily_max)
    ctw = result['current_target_week'] = get_next_target(cwc, weekly_max)
    ctm = result['current_target_month'] = get_next_target(cmc, monthly_max)
    cty = result['current_target_year'] = get_next_target(cyc, yearly_max)

    result['today_lpd'] = get_lpd_arr(ctd, daily_max)
    result['current_week_lpd'] = get_lpd_arr(ctw, weekly_max)
    result['current_month_lpd'] = get_lpd_arr(ctm, monthly_max)
    result['current_year_lpd'] = get_lpd_arr(cty, yearly_max)


    # for display purpose only. Show current day
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fir', 'Sat', 'Sun']
    result['weekday'] = days[today.weekday()]
    """
        CHRIS PANTAZIS CODE ENDS HERE
    """
    cache.set(cache_key, result, 600)
    return result


def get_next_target(curr_val, maximums):
    i = m = 0
    for m in maximums:
        if m < curr_val:
            i += 1
        else:
            break
    return m


def get_lpd_arr(val, arr):
    """
    Author: Chris Pantazis (07/08/2014)
    This function returns an array of literals depending on
    the target consumption per person per day for the current household.
    This is actually a workaround.
    Needed in <<summary.html>> template file to print correct number of smilies

    :param val: Total consumption for period (float)
    :param arr: array with maximum targets for given period
    :return: array that has a len of 5,4,3,2,1 or 0 for number of smilies
    """
    lpd = []
    # how many smilies user loses? 1 for every maximum lost
    x = arr.index(int(val))
    y = len(arr)
    for a in range(y - x):
        lpd.append(a)
    return lpd

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

