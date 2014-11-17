__author__ = 'chris'
from django.conf.urls import patterns, include, url
from uc_03_6.views import user_events, event_history


urlpatterns = patterns(
    '',
    # Examples:
    url(r'^events/(\w+)/$', user_events, name='user_events'),
    url(r'^events/history/(\w+)/$', event_history, name='fault_history'),
)
