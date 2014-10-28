from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from iwidget.models import UserValidationKey
import os
from os import path
import unicodecsv as csv
import binascii


class Command(BaseCommand):
    help = 'Command that creates passwords for meter ids in a csv file'

    def handle(self, *args, **options):
        try:
            _range = args[0]
        except IndexError:
            print "Please, provide a user id range"
            return
        _min = _range.split('-')[0]
        _max = _range.split('-')[1]
        try:
            users = User.objects.filter(id__gte=_min, id__lte=_max)\
                .order_by("username")
            out = []
            for user in users:
                try:
                    uvk = UserValidationKey.objects.get(user=user)
                    key = uvk.key
                    val = str(binascii.hexlify(os.urandom(4)).upper())
                    email = "M%s@example.com" % val
                    out.append([user.username, key, email])
                except UserValidationKey.DoesNotExist:
                    continue
            import time
            ts = int(time.time())
            _outfile = "exported_password_%s.csv" % ts
            _path = "data/"
            with open(path.join(_path, _outfile), 'w') as of:
                a = csv.writer(of, delimiter=',',
                               quotechar='"',
                               quoting=csv.QUOTE_ALL)
                a.writerows(out)
        except Exception as e:
            raise CommandError(repr(e))
