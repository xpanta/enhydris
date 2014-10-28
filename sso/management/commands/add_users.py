__author__ = 'chris'
from django.core.management.base import BaseCommand, CommandError
import requests
import logging
from iwidget.models import UserValidationKey
from xml.dom import minidom
import time
from sso.common import encrypt_and_hash_pwd


class Command(BaseCommand):
    help = 'Command that adds a Caller Application in the SSO service'

    def handle(self, *args, **options):
        log = logging.getLogger(__name__)

        try:
            name_keys = UserValidationKey.objects.filter(sso=False)\
                .values('user__username', 'key')
            print "found %s users to add" % len(name_keys)
            headers = {'Content-Type': 'text/xml'}
            xml_data = """<?xml version="1.0" encoding="utf-8"?><soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body><AddUser xmlns="https://services.up-ltd.co.uk/adminservice_iwidget/"><name>##USER##</name><password>##PASSWORD##</password><serviceUsername>IWidgetService</serviceUsername><servicePassword>1-Widg3t##Crypt0Service</servicePassword></AddUser></soap:Body></soap:Envelope>"""
            #nk = {
            #    "user__username": "superuser",
            #    "key": "@super.@user"
            #}
            #name_keys = [nk]
            for name_key in name_keys:
                name = name_key['user__username']
                key = name_key['key']
                #name = "test_user"
                #key = "test_pwd"
                enc_pwd = encrypt_and_hash_pwd(key)
                time.sleep(1)
                #print "sending request for %s with pwd %s" % (name, enc_pwd)
                data = xml_data
                data = data.replace("##USER##", name)
                data = data.replace("##PASSWORD##", enc_pwd)
                print data
                res = requests.post('https://services.up-ltd.co.uk/'
                                    'adminservice_iwidget/service.asmx',
                                    data=data, headers=headers)
                #print res.text
                if res.status_code == requests.codes.ok:
                    doc = minidom.parseString(res.text)
                    result = doc.getElementsByTagName("AddUserResult")[0]
                    val = result.firstChild.data
                    print "for user %s, response was %s" % (name, val)
                    print "updating HH database"
                    uvk = UserValidationKey.objects\
                        .get(user__username=name)
                    uvk.sso = True
                    uvk.save()
                    time.sleep(1)
                #print res.text
        except Exception as e:
            print repr(e)
