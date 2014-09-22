__author__ = 'chris'
from django.core.management.base import BaseCommand, CommandError
import os
from os import path
import binascii
import unicodecsv as csv


class Command(BaseCommand):
    help = 'Command that creates passwords for meter ids in a csv file'

    def handle(self, *args, **options):
        try:
            _filename = "uk.csv"
            _outfile = "test.csv"
            _path = "data/southern/"
            with open(path.join(_path, _filename), 'r') as f:
                meter_ids = []
                data = csv.reader(f, encoding="utf-8")
                for row in data:
                    meter_ids.append(row[0])

            with open(path.join(_path, _outfile), 'w') as of:
                a = csv.writer(of, delimiter=',',
                               quotechar='"',
                               quoting=csv.QUOTE_ALL)
                out = []
                used = []
                for mid in meter_ids:
                    if mid not in used:
                        key = binascii.hexlify(os.urandom(5))
                        out.append([mid, key])
                        used.append(mid)
                a.writerows(out)
        except Exception as e:
            raise CommandError(repr(e))
