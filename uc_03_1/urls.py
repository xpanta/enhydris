__author__ = 'chris'
from django.conf.urls import patterns, include, url
from uc_03_1.views import compare


urlpatterns = patterns(
    '',
    # Examples:
    url(r'^compare/(\w+)/$', compare, name='uc_03_1_compare'),
)

