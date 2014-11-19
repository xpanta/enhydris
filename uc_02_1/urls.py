__author__ = 'chris'
from django.conf.urls import patterns, include, url
from uc_02_1.views import calc_costs


urlpatterns = patterns(
    '',
    # Examples:
    url(r'^analyse/(\w+)/$', calc_costs, name='uc_02_1_calc'),
)
