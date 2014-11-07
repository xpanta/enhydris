from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required
from unexe.views import *
from django.contrib import admin
from iwidget import views as iwidget_views
from iwidget.views import TimeseriesDetailView
""" Added by Chris Pantazis to redirect signup/ to core/signup. Why?
    because it is easier for the user to remember that
"""
from django.views.generic.base import RedirectView

#from enhydris.iwidget.views import (timeseries_detail, index,
#        household_view, dma_view, household_properties)

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'iwidget_consumer.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^test$', test.as_view(), name='test'),  # logout
    url(r'^$', home.as_view(), name='home'),  # home page
    url(r'^dashboard$', login_required(dashboard.as_view()),
        name='dashboard'),  # consumer dashboard
    url(r'^dashboard/d/(?P<household_id>\d+)/$',
        login_required(dashboard.as_view()),
        name='dashboard'),  # consumer dashboard
    url(r'^logout$', logout.as_view(), name='logout'),  # logout
    #url(r'^super/$', login.as_view(), name='adminlogin'),  # logout
    url(r'^login/$', RedirectView.as_view(
        url='https://services.up-ltd.co.uk/iwidget/?c=hhApp', permanent=False),
        name='login'),
    #url(r'^login$', login.as_view(), name='login'),  # logout
    url(r'^changepassword$', login_required(changepassword.as_view()),
        name='changepassword'),  # changepassword
    url(r'^updateuser$', login_required(updateuser.as_view()),
        name='updateuser'),  # changepassword
    url(r'^getuser$', login_required(getuser.as_view()),
        name='getuser'),  # getuser
    url(r'^gethousehold$', login_required(gethousehold.as_view()),
        name='gethousehold'),  # gethousehold
    url(r'^updatehousehold$', login_required(updatehousehold.as_view()),
        name='updatehousehold'),  # getuser
    url(r'^policy$', login_required(policy.as_view()),
        name='policy'),  # policy
    url(r'^dmas/d/(?P<dma_id>\d+)/$', login_required(dmas.as_view()),
        name='dmas'),  # dmas
    url(r'^usersuper$', login_required(usersuper.as_view()),
        name='usersuper'),  # dmas
    url(r'^timeseries/d/(?P<object_id>\d+)/$',
        login_required(timeseries.as_view()), name='timeseries'),  # dmas
    url(r'^getcompare$', login_required(getcompare.as_view()),
        name='getcompare'),  # getcompare
    url(r'^c_uc53$', login_required(c_uc53.as_view()),
        name='c_uc53'),  # getforecast
    url(r'^c_uc52$', login_required(c_uc52.as_view()),
        name='c_uc52'),  # getcompare
    url(r'^c_uc33$', login_required(c_uc33.as_view()),
        name='c_uc33'),  # getcompare
    url(r'^c_uc32$', login_required(c_uc32.as_view()),
        name='c_uc32'),  # getcompare
    
    url(r'^c_uc34$', login_required(c_uc34.as_view()),name='c_uc34'),
    url(r'^c_uc41$', login_required(c_uc41.as_view()),name='c_uc41'),
    url(r'^c_uc54$', login_required(c_uc54.as_view()),name='c_uc54'),        
                           
    url(r'^ukcsregistration$', ukcsregistration.as_view(),name='ukcsregistration'), 
    url(r'^ukcsregistrationsave$', ukcsregistrationsave.as_view(),name='ukcsregistrationsave'),
    url(r'^ukcsregistrationconfirm$', ukcsregistrationconfirm.as_view(),name='ukcsregistrationconfirm'),
                       
    url(r'^admin/',include(admin.site.urls)),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    
    url(r'^ajax/', include('ajax_select.urls')),
    url(r'^api/', include('enhydris.api.urls')),
    url(r'', include('enhydris.hcore.urls')),
    
    url(r'^ajax/period_stats/$', iwidget_views.periods_distribution,
        {}, 'periods_distribution'),
    
    url(r'^household/d/(?P<household_id>\d+)/$',
        iwidget_views.household_view, {}, 'household_view'),
    url(r'^dma/d/(?P<dma_id>\d+)/$', iwidget_views.dma_view, {}, 'dma_view'),
    url(r'^household/properties/update/$',
        iwidget_views.household_properties, {}, 'household_properties'),

    # Added by Chris Pantazis to redirect to core/signup
    #url(r'^signup/$', RedirectView.as_view(url='/core/signup/',
    #                                       permanent=False)),
)

""" url confs from other use cases go here """

urlpatterns += patterns(
    "",
    url(r'^uc_03_1/',include('uc_03_1.urls')),
    url(r'^uc_03_6/',include('uc_03_6.urls')),
    url(r'^core/',include('core.urls')),
)