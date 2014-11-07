__author__ = 'chris'
from django.conf.urls import patterns, include, url
from uc_03_6.views import user_events


urlpatterns = patterns(
    '',
    # Examples:
    url(r'^events/(\w+)/$', user_events, name='user_events'),
)
