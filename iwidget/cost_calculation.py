# -*- coding: utf-8 -*-
#!/usr/bin/python

# iWidget application for openmeteo Enhydris software
# This software is provided with the AGPL license
# Copyright (c) 2013-2014 National Techincal University of Athens

import math

from pthelma.timeseries import Timeseries, TimeStep

CUBIC_METER_FLAT_RATE = 0.40
KWH_FLAT_RATE = 0.10

def monthly_cost_from_consumption(consumption, rate=CUBIC_METER_FLAT_RATE):
    """
    Calculates the monthly cost from monthly consumption. Consumption
    in cubic meters, returns cost in Euro
    """
    if math.isnan(consumption):
        return 0.0
    return consumption * rate

def calculate_cost_timeseries(consumption_timeseries,
        rate=CUBIC_METER_FLAT_RATE):
    timestep_kwargs = dict([
            (attr, getattr(consumption_timeseries.time_step, attr))
            for attr in ('length_minutes', 'length_months',
            'interval_type', 'nominal_offset', 'actual_offset')])
    time_step = TimeStep(**timestep_kwargs)
    result = Timeseries(time_step = time_step)
    for timestamp in consumption_timeseries:
        result[timestamp] = monthly_cost_from_consumption(
                consumption_timeseries[timestamp], rate=rate)
    return result

