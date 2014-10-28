__author__ = 'chris'
from django.core.management.base import BaseCommand, CommandError
import os
from os import path
import binascii
import unicodecsv as csv
from iwidget.models import UserValidationKey
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Command that creates passwords for meter ids in a csv file'

    def handle(self, *args, **options):
        try:
            uid = args[0]
        except KeyError:
            print "I need a user id"
            return 1

        try:
            user = User.objects.get(username=uid)
        except User.DoesNotExist:
            print "User not found!"
            return 1

        key = "iwidgetuser"
        ser = user.username
        uvk = UserValidationKey.objects.create(user=user, key=key,
                                               identifier=ser)
        print "Done (%s)!" % key
        return 0
