___author__ = 'chris'
from django.core.management.base import BaseCommand, CommandError
import requests
import os
from os import path
import logging

class Command(BaseCommand):
    help = 'Command that adds a Caller Application in the SSO service'

    def handle(self, *args, **options):
        log = logging.getLogger(__name__)
        try:
            _filename = args[0]
        except IndexError:
            print "please specify a file"
            return
        try:
            _path = "sso/"
            with open(path.join(_path, _filename), 'r') as f:
                # readlines() is not the best, but xml files are small
                data = ''
                for line in f:
                    data += line.strip()
                # what the server accepts
                headers = {'Content-Type': 'text/xml'}
                res = requests.post('https://services.up-ltd.co.uk/'
                                    'adminservice_iwidget/service.asmx',
                                    data=data, headers=headers)
                print res
                print res.text
        except Exception as e:
            print repr(e)
