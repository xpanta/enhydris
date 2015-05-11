__author__ = 'Chris Pantazis'
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from iwidget.models import UserValidationKey
import requests
import os
from os import path
import logging


class Command(BaseCommand):
    help = 'Command that adds a Caller Application in the SSO service'

    def handle(self, *args, **options):
        log = logging.getLogger(__name__)
        try:
            username = args[0]
            pwd = args[1]
        except IndexError:
            return -1
        user = User.objects.get(username=username)
        user.set_password(pwd)
        user.save()
        from sso.common import encrypt_and_hash_pwd
        import requests
        from xml.dom import minidom
        xml = """<?xml version="1.0" encoding="utf-8"?><soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body><SetUserPassword xmlns="https://services.up-ltd.co.uk/adminservice_iwidget/"><name>##USER##</name><password>##PASSWORD##</password><serviceUsername>IWidgetService</serviceUsername><servicePassword>1-Widg3t##Crypt0Service</servicePassword></SetUserPassword></soap:Body></soap:Envelope>"""
        enc_pwd = encrypt_and_hash_pwd(pwd)
        xml = xml.replace("##USER##", user.username) \
            .replace("##PASSWORD##", enc_pwd)
        headers = {'Content-Type': 'text/xml'}
        res = requests.post('https://services.up-ltd.co.uk/'
                            'adminservice_iwidget/service.asmx',
                            data=xml, headers=headers)
        if res.status_code == requests.codes.ok:
            doc = minidom.parseString(res.text)
            result = doc.getElementsByTagName("SetUserPasswordResult")[0]
            val = result.firstChild.data
            if val == "true":  # True only if SSO update was OK!!
                status = True
                try:
                    uvk = UserValidationKey. \
                        objects.get(user=user)
                    uvk.key = pwd
                    uvk.save()
                except UserValidationKey.DoesNotExist:
                    uvk = UserValidationKey. \
                        objects.create(user=user,
                                       identifier="",
                                       key=pwd,
                                       sso=True,
                                       popup=False)
            else:
                status = False
