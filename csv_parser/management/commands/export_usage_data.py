__author__ = 'Chris Pantazis'
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from iwidget.models import UsageData, UserPageView
import os
from os import path
import unicodecsv as csv
import binascii


class Command(BaseCommand):
    help = 'Command that exports usage data for meter ids in a csv file'

    def handle(self, *args, **options):
        try:
            code = args[0]
        except IndexError:
            print "Please, provide a country code id range"
            return
        try:
            users = User.objects.filter(username__startswith=code) \
                .order_by("username")
            for user in users:
                out = []
                try:
                    logins = UsageData.objects.filter(user=user)
                    for login in logins:
                        out.append([user.username,
                                    login.enter_ts, login.exit_ts])
                except UsageData.DoesNotExist:
                    continue
                _outfile = "%s_usage_data.csv" % user.username
                _path = "data/usage/%s" % code
                with open(path.join(_path, _outfile), 'w') as of:
                    a = csv.writer(of, delimiter=',',
                                   quotechar='"',
                                   quoting=csv.QUOTE_ALL)
                    a.writerows(out)
                    # PAGE VIEWS
            for user in users:
                out = []
                try:
                    page_views = UserPageView.objects.filter(user=user)
                    for pv in page_views:
                        out.append([user.username, pv.page, pv.added])
                except UserPageView.DoesNotExist:
                    continue
                _outfile = "%s_page_views.csv" % user.username
                _path = "data/usage/%s" % code
                with open(path.join(_path, _outfile), 'w') as of:
                    a = csv.writer(of, delimiter=',',
                                   quotechar='"',
                                   quoting=csv.QUOTE_ALL)
                    a.writerows(out)
        except Exception as e:
            raise CommandError(repr(e))
