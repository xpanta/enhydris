__author__ = 'chris'
import requests
from xml.dom import minidom
from hashlib import sha512

def encrypt_and_hash_pwd(pwd):
    """
        Encrypts passwords with the use of SSO
    """
    try:
        xml = """<?xml version="1.0" encoding="utf-8"?><soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body><Encrypt xmlns="https://services.up-ltd.co.uk/cryptoservice_iwidget/"><PlainText>%%PASSWORD%%</PlainText></Encrypt></soap:Body></soap:Envelope>"""
        xml = xml.replace("%%PASSWORD%%", pwd)
        url = "https://services.up-ltd.co.uk/cryptoservice_iwidget/service.asmx"
        headers = {'Content-Type': 'text/xml'}
        res = requests.post(url, data=xml, headers=headers)
        if res.status_code == requests.codes.ok:
            doc = minidom.parseString(res.text)
            result = doc.getElementsByTagName("EncryptResult")[0]
            encrypted_pwd = result.firstChild.data
            return sha512(encrypted_pwd).hexdigest()
    except Exception as e:
        print repr(e)
        return None

