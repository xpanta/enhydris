__author__ = 'chris'
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from iwidget.models import UserValidationKey
from os import path
import unicodecsv as csv


class Command(BaseCommand):
    help = 'Command that updates passwords from csv file'

    def handle(self, *args, **options):
        try:
            _filename = "keys.csv"
            _path = "data/southern/"
            with open(path.join(_path, _filename), 'r') as f:
                c = 0
                data = csv.reader(f, encoding="utf-8")
                for row in data:
                    username = row[0]
                    key = row[1]
                    try:
                        user = User.objects.get(username=username)
                    except User.DoesNotExist:
                        print "*** not found: %s" % username
                        c += 1
                        continue
                    uvk = UserValidationKey.objects.get(user=user)
                    uvk.key = key
                    uvk.save()
            print "not found total %s" % c
        except Exception as e:
            raise CommandError(repr(e))
