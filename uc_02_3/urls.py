__author__ = 'chris'
from django.conf.urls import patterns, include, url
from uc_02_3.views import calc_carbon


urlpatterns = patterns(
    '',
    # Examples:
    url(r'^analyse/(\w+)/$', calc_carbon, name='uc_02_3_calc'),
)
