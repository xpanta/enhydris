__author__ = 'Chris Pantazis'
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from iwidget.models import Household


class Command(BaseCommand):
    help = 'Command that deletes houehold data for a user'

    def handle(self, *args, **options):
        try:
            username = args[0]
        except IndexError:
            print "I need a username!"
            return -1
        try:
            if username:
                user = User.objects.get(username=username)
                household = Household.objects.get(user=user)
                print "deleting data for {x} and hh id {y}"\
                    .format(
                        x=username,
                        y=household.id
                    )
                household.delete()
        except Exception as e:
            print "failed with %s" % repr(e)
