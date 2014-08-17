#from django.core.exceptions import ImproperlyConfigured
#from django.conf import settings
#from datetime import datetime, timedelta
#import json
#import urllib2
import base64
from suds.client import Client 

class irest():
        
    def __init__(self, serviceURL, username="", password=""):
        self.username  = username
        self.password  = password        
        self.client    = Client(serviceURL)  #username=self.username,password=self.password)
        
    def addUser(self, userid, passwd):
        self.client.service.AddUser(userid,passwd,self.username,self.password)
    
    def getUser(self, userid):
        return self.client.service.GetUsers(self.username,self.password)