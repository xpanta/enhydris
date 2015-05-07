__author__ = 'Chris Pantazis'
from django.conf.urls import patterns, include, url
from iw_admin.views import usage_data


urlpatterns = patterns(
    '',
    # Examples:
    url(r'^data/usage/(\w+)/$', usage_data, name='usage_data'),
)
