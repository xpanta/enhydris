#!/usr/bin/python

# iWidget application for openmeteo Enhydris software
# This software is provided with the AGPL license
# Copyright (c) 2013 National Techincal University of Athens

# Calculates occupancy based on an average water consumption,
# for each household

import math

from django.core.management.base import BaseCommand
from django import db

from iwidget.models import Household, TSTEP_DAILY

from pthelma.timeseries import timeseries_bounding_dates_from_db
from pthelma.timeseries import Timeseries as TSeries

AVERAGE_UNIT_WATER_CONSUMPTION = 180.000

def process():
    for household in Household.objects.all():
        daily_series_db = household.timeseries.get(
                time_step__id=TSTEP_DAILY)
        series = TSeries(id=daily_series_db.id)
        series.read_from_db(db.connection)
        m = 1000.000*series.average()
        if math.isnan(m):
            continue
        num_of_occupants = max(1,
                int(round(m/AVERAGE_UNIT_WATER_CONSUMPTION)))
        print 'Household with id=%s, average daily consumption %.1f, '\
              'number of occupants set to %s'%(household.id, m,
                      num_of_occupants,)
        household.num_of_occupants = num_of_occupants
        household.save()

class Command(BaseCommand):
    args = ''
    help = 'Calculates occupancy based on an average water consumption, '\
           'for each household'

    def handle(self, *args, **options):
        options['handle'] = self
        process()
