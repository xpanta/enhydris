__author__ = 'Chris Pantazis'
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from iwidget.models import Household, VAR_PERIOD, TSTEP_FIFTEEN_MINUTES, \
    TSTEP_HOURLY
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
            code = args[0]
        except IndexError:
            print "I need a country code!"
            return -1
        try:
            if code:
                users = User.objects.filter(username__startswith=code)
                out = []
                for user in users:
                    household = Household.objects.get(user=user)
                    out.append([user.username, household.id])
                _outfile = "HH_ids_%s.csv" % code
                _path = "data/"
                with open(path.join(_path, _outfile), 'w') as of:
                    a = csv.writer(of, delimiter=',',
                                   quotechar='"',
                                   quoting=csv.QUOTE_ALL)
                    a.writerows(out)
        except Exception as e:
            print "failed with %s" % repr(e)
