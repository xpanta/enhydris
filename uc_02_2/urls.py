from django.conf.urls import patterns, include, url
from uc_02_2.views import calculate_appliance_energy as cae


urlpatterns = patterns(
    '',
    # Examples:
    url(r'^analyse/(\w+)/$', cae, name='uc_02_2_cae'),
)

