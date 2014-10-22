__author__ = 'chris'
from django.conf.urls import patterns, url
from core.views import signup, sso_redirect, user_profile


urlpatterns = patterns(
    '',
    # Examples:
    url(r'^signup/$', signup, name='signup'),
    url(r'^sso/auth/$', sso_redirect, name='sso_redirect'),
    url(r'^user/profile/$', user_profile, name='user_profile'),
)
