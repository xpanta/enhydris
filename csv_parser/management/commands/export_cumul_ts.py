__author__ = 'Chris Pantazis'
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from iwidget.models import Household, VAR_CUMULATIVE, TSTEP_FIFTEEN_MINUTES
from os import path
from django import db
import unicodecsv as csv
from pthelma.timeseries import Timeseries as TSeries
import numpy as np
from math import isnan

class Command(BaseCommand):
    help = 'Command that exports last import timeseries for a users in a ' \
           'csv file'

    def handle(self, *args, **options):
        try:
            username = args[0]
        except IndexError:
            print "I need a username!"
            return -1
        try:
            if username:
                user = User.objects.get(username=username)
                out = []
                print "output for {x}".format(x=username)
                household = Household.objects.get(user=user)
                # ts_raw = household.timeseries.filter(time_step__isnull=True,
                #                                      variable__id=VAR_CUMULATIVE)[0]
                # series = TSeries(id=ts_raw.id)
                timeseries = household \
                    .timeseries.get(variable__id=VAR_CUMULATIVE)
                series = TSeries(id=timeseries.id)
                series.read_from_db(db.connection)
                timestamps = sorted(series.keys())
                values = np.array([])
                for ts in timestamps:
                    val = series[ts]
                    if isnan(val) or val == 0:
                        continue
                    values = np.append(values, val)
                    #perc = np.percentile(values, 90)
                    out.append([ts, val])
                _outfile = "timeseries_cumulative_%s.csv" % username
                _path = "data/"
                with open(path.join(_path, _outfile), 'w') as of:
                    a = csv.writer(of, delimiter=',',
                                   quotechar='"',
                                   quoting=csv.QUOTE_ALL)
                    a.writerows(out)
        except Exception as e:
            print "failed with %s" % repr(e)
