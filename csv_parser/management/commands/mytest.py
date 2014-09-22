__author__ = 'chris'
from django.core.management.base import BaseCommand, CommandError
from django.utils.dateparse import parse_datetime
import csv
import pytz
import calendar


class Command(BaseCommand):
    help = 'This is just a test!'

    def handle(self, *args, **options):
        try:
            print "hello!"
        except Exception as e:
            raise CommandError(repr(e))
