from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.generics import RetrieveAPIView
from enhydris.hcore import models
from iwidget import models as iwidget_models
from enhydris.api.views import modelnames, TimeseriesList, TimeseriesDetail,\
    Tsdata, ListAPIView
from enhydris.api import serializers

_urls = ['enhydris.api.views',
         url(r'^$', 'api_root'),
         url(r'^tsdata/(?P<pk>\d+)/$', Tsdata.as_view(), name='tsdata')]
all_models = dict((x, models.__dict__[x]) for x in models.__dict__)
all_models.update(dict((x, iwidget_models.__dict__[x]) for x in iwidget_models.__dict__))
for _x in modelnames:
    model = all_models[_x]
    serializer_class = None
    if _x == 'Station':
        serializer_class = serializers.StationSerializer
    detail_view = RetrieveAPIView.as_view(model=model,
                                          serializer_class=serializer_class)
    list_view = ListAPIView.as_view(model=model,
                                    serializer_class=serializer_class)
    if _x == 'Timeseries':
        list_view = TimeseriesList.as_view()
        detail_view = TimeseriesDetail.as_view()
    _urls.append(url(r'^{0}/$'.format(_x), list_view, name=_x + '-list'))
    _urls.append(url(r'^{0}/modified_after/(?P<modified_after>.*)/$'
                     .format(_x), list_view, name=_x + '-list'))
    _urls.append(url(r'^{0}/(?P<pk>\d+)/$'.format(_x), detail_view,
                     name=_x + '-detail'))

urlpatterns = format_suffix_patterns(patterns(*_urls))
