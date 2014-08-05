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
    cache.set(cache_key, result, 600)
    return result

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

