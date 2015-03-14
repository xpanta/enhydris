__author__ = 'Chris Pantazis'
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from iwidget.models import UserValidationKey


class Command(BaseCommand):
    help = 'Command that exports last import dates for all users in a csv file'

    def handle(self, *args, **options):
        try:
            users = User.objects.filter(username__startswith='00')
            for user in users:
                user.set_password('iwidgetuser')
                user.save()
                UserValidationKey.objects.get_or_create(
                    user=user,
                    key='iwidgetuser',
                    identifier=user.username,
                )
        except Exception as e:
            raise CommandError(repr(e))
