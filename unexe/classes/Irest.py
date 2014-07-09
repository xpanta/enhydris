from django.core.exceptions import ImproperlyConfigured
from django.conf import settings
from datetime import datetime, timedelta
import json
import urllib2

class irest():    
    def __init__(self):
        self.test = "1"
