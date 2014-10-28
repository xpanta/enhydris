__author__ = 'chris'
from django.core.management.base import BaseCommand, CommandError
from iwidget.models import UserValidationKey


class Command(BaseCommand):
    help = 'Command that updates users passwords from validation keys'

    def handle(self, *args, **options):
        print "starting..."
        try:
            rows = UserValidationKey.objects.all()
            for row in rows:
                key = row.key
                user = row.user
                user.set_password(key)
                user.save()
            print "Done!"
        except Exception as e:
            raise CommandError(repr(e))
