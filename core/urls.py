__author__ = 'chris'
from django.conf.urls import patterns, url
from core.views import signup, sso_redirect, user_profile, \
    reset_form, user_exits, add_page_view


urlpatterns = patterns(
    '',
    # Examples:
    url(r'^signup/$', signup, name='signup'),
    url(r'^sso/auth/$', sso_redirect, name='sso_redirect'),
    url(r'^user/profile/$', user_profile, name='user_profile'),
    url(r'^user/recover/$', reset_form, name='reset_form'),
    url(r'^user/exits/$', user_exits, name='user_exits'),
    url(r'^user/page/view/$', add_page_view, name='user_page_view'),
)
