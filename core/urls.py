__author__ = 'chris'
from django.conf.urls import patterns, url
from core.views import signup, sso_redirect, user_profile, reset_form


urlpatterns = patterns(
    '',
    # Examples:
    url(r'^signup/$', signup, name='signup'),
    url(r'^sso/auth/$', sso_redirect, name='sso_redirect'),
    url(r'^user/profile/$', user_profile, name='user_profile'),
    url(r'^user/recover/$', reset_form, name='reset_form'),
)
