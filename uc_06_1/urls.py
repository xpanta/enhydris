__author__ = 'chris'
from django.conf.urls import patterns, include, url
from uc_06_1.views import get_plegma_devices


urlpatterns = patterns(
    '',
    # Examples:
    url(r'^devices/get/(\w+)/$', get_plegma_devices, name='uc_06_1_get'),
)
