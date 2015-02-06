__author__ = 'Chris Pantazis'
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from iwidget.models import Household, VAR_PERIOD, VAR_ENERGY_PERIOD, \
    VAR_CUMULATIVE, VAR_ENERGY_CUMULATIVE
from pthelma.timeseries import timeseries_bounding_dates_from_db
from os import path
from django import db
import unicodecsv as csv


class Command(BaseCommand):
    help = 'Command that exports last import dates for all users in a csv file'

    def handle(self, *args, **options):
        try:
            prefix = args[0]
        except IndexError:
            prefix = ""
        try:
            if prefix:
                users = User.objects.filter(username__icontains=prefix)
            else:
                users = User.objects.all()
            out = []
            for user in users:
                household = Household.objects.get(user=user)
                s1 = e1 = None
                try:
                    for variable in (VAR_PERIOD, VAR_ENERGY_PERIOD):
                        if variable == VAR_PERIOD:
                            _type = "WATER"
                        else:
                            _type = "ENERGY"
                        raw_series_db = household.timeseries.filter(
                            time_step__isnull=True,
                            variable__id={
                                VAR_PERIOD: VAR_CUMULATIVE,
                                VAR_ENERGY_PERIOD: VAR_ENERGY_CUMULATIVE
                            }[variable])[:1]
                        if not raw_series_db:
                            continue
                        raw_series_db = raw_series_db[0]
                        s1, e1 = timeseries_bounding_dates_from_db(
                            db.connection, raw_series_db.id)
                        if s1:
                            start = s1.strftime("%Y-%m-%d %H:%M:%S")
                        else:
                            start = ""
                        if e1:
                            end = e1.strftime("%Y-%m-%d %H:%M:%S")
                        else:
                            end = ""
                        out.append([user.username, start, end, _type])
                except Exception as e:
                    print (repr(e))
                    continue
            import time
            ts = int(time.time())
            _outfile = "%s_last_imported_dates_%s.csv" % (prefix, ts)
            _path = "data/"
            with open(path.join(_path, _outfile), 'w') as of:
                a = csv.writer(of, delimiter=',',
                               quotechar='"',
                               quoting=csv.QUOTE_ALL)
                a.writerows(out)
        except Exception as e:
            raise CommandError(repr(e))
