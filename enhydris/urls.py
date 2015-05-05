from django.conf.urls import include, patterns, url
from django.contrib.auth.views import password_reset, password_reset_done, \
    password_change, password_change_done
from django.contrib import admin
from django.conf import settings
from registration.views import RegistrationView
#from profiles.views import create_profile, edit_profile
from enhydris.hcore.forms import RegistrationForm
from enhydris.hcore.views import terms, login

from iwidget.views import (TimeseriesDetailView, index, household_view,
                           dma_view, household_properties,
                           periods_distribution, user_logout)

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', index, {}, 'index'),
    url(r'^timeseries/d/(?P<pk>\d+)/$', TimeseriesDetailView.as_view(),
        name='timeseries_detail'),
    url(r'^household/d/(?P<household_id>\d+)/$',
        household_view, {}, 'household_view'),
    url(r'^dma/d/(?P<dma_id>\d+)/$',
        dma_view, {}, 'dma_view'),
    url(r'^household/properties/update/$',
        household_properties, {}, 'household_properties'),
    url(r'^ajax/period_stats/$', periods_distribution, {},
        'periods_stats'),
    url(r'^accounts/login/$', login,
        {'template_name': 'registration/login.html'}, 'login'),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^accounts/password/reset/$', password_reset,
        {'template_name': 'registration/password_reset.html'},
        'password_reset'),
    url(r'^accounts/password/reset/done/$', password_reset_done,
        {'template_name': 'registration/password_reset_done.html'},
        'password_reset_done'),
    url(r'^accounts/password/change/$', password_change,
        {'template_name': 'registration/password_change.html'},
        'password_change'),
    url(r'^accounts/password/change/done/$', password_change_done,
        {'template_name': 'registration/password_change_done.html'},
        'password_change_done'),
    url(r'^accounts/', include('registration.backends.default.urls')),

    # django profiles
    # to enable django <-> site admin overlapping
    #(r'^profiles/admin/(.*)', admin.site.root),
    #(r'^profile/', include('profiles.urls')),
#    (r'^profile/create/$', create_profile, {}, 'profiles_create_profile'),
#    (r'^profile/edit/$', edit_profile, {}, 'profiles_edit_profile'),
#    (r'^profile/(?P<username>\w+)/$', profile_view, {},
#                                 'profiles_profile_detail'),
    url(r'^profile/', include('profiles.urls')),
    # terms of usage
    url(r'^terms/$', terms, {}, 'terms'),
    # internationalization
    url(r'^i18n/', include('django.conf.urls.i18n')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
#    (r'^grappelli/', include('grappelli.urls')),
    url(r'^ajax/', include('ajax_select.urls')),
    url(r'^api/', include('enhydris.api.urls')),
    url(r'', include('enhydris.hcore.urls')),
)
if getattr(settings, 'REGISTRATION_OPEN', True):
    urlpatterns = patterns(
        '',
        url(r'^accounts/register/$',
            RegistrationView.as_view(form_class=RegistrationForm),
            name='registration_register')) + urlpatterns



from enhydris.settings import DEBUG, MEDIA_ROOT, STATIC_ROOT
if DEBUG:
    urlpatterns += patterns(
        '',
        url(
            r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {
                'document_root': MEDIA_ROOT,
            }
        ),
        url(
            r'^static/(?P<path>.*)$', 'django.views.static.serve',
            {
                'document_root': STATIC_ROOT,
            }
        ),
    )
