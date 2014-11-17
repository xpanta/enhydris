__author__ = 'chris'
from django.conf.urls import patterns, include, url
from uc_01_2.views import calculate_appliance_consumption as cac


urlpatterns = patterns(
    '',
    # Examples:
    url(r'^analyse/(\w+)/$', cac, name='uc_01_2_cac'),
)
