__author__ = 'chris'
from django.conf.urls import patterns, include, url
from core.views import signup, user_profile


urlpatterns = patterns(
    '',
    # Examples:
    url(r'^signup/$', signup, name='signup'),
    url(r'^user/profile/(\w+)/$', user_profile, name='user_profile'),
)
