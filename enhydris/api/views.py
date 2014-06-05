from StringIO import StringIO

from django.http import Http404, HttpResponse
from django.db import connection
from django.shortcuts import get_object_or_404

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from pthelma.timeseries import Timeseries
from enhydris.hcore import models
from enhydris.api.permissions import CanEditOrReadOnly


modelnames = (
    'Lookup Lentity Person Organization Gentity Gpoint Gline Garea '
    'PoliticalDivisionManager PoliticalDivision WaterDivision WaterBasin '
    'GentityAltCodeType GentityAltCode FileType GentityFile EventType '
    'GentityEvent StationType StationManager Station Overseer InstrumentType '
    'Instrument Variable UnitOfMeasurement TimeZone TimeStep Timeseries'
).split()


@api_view(('GET',))
def api_root(request, format=None):
    d = {}
    for m in modelnames:
        d[m] = reverse(m + '-list', request=request, format=format)
    return Response(d)


class ListAPIView(generics.ListAPIView):

    def get_queryset(self):
        modified_after = '1900-01-01'
        if 'modified_after' in self.kwargs:
            modified_after = self.kwargs['modified_after']
        return self.model.objects.exclude(last_modified__lte=modified_after)


class Tsdata(APIView):
    """
    Take a timeseries id and return the actual timeseries data to the client,
    or update a time series with new records.
    """
    permission_classes = (CanEditOrReadOnly,)

    def get(self, request, pk, format=None):
        ts = Timeseries(id=int(pk))
        self.check_object_permissions(request, ts)
        ts.read_from_db(connection)
        result = StringIO()
        ts.write(result)
        return HttpResponse(result.getvalue(), content_type="text/plain")

    def put(self, request, pk, format=None):
        try:
            ts = Timeseries(id=int(pk))
            self.check_object_permissions(request, ts)
            result_if_error = status.HTTP_400_BAD_REQUEST
            ts.read(StringIO(request.DATA['timeseries_records']))
            result_if_error = status.HTTP_409_CONFLICT
            ts.append_to_db(connection, commit=False)
            return HttpResponse(str(len(ts)), content_type="text/plain")
        except ValueError as e:
            return HttpResponse(status=result_if_error,
                                content=str(e),
                                content_type="text/plain")

    def post(self, request, pk, format=None):
        """
        We temporarily keep post the same as put so that older
        versions of loggertodb continue to work
        """
        return self.put(request, pk, format=None)


class TimeseriesList(generics.ListCreateAPIView):
    model = models.Timeseries
    permission_classes = (CanEditOrReadOnly,)

    def post(self, request, *args, **kwargs):
        """
        Redefine post, checking permissions.
        Django-rest-framework does not do object-level permission when
        creating a new object, so we have to completely customize the post
        method. Maybe there's a better way, such as using a mixin for the
        functionality below (especially when the API is extended to include
        other types as well).
        """
        # Get the data
        serializer = self.get_serializer(data=request.DATA,
                                         files=request.FILES)
        if not serializer.is_valid():
            Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Check permissions
        try:
            gentity_id = int(serializer.init_data['gentity'])
        except ValueError:
            raise Http404
        station = get_object_or_404(models.Station, id=gentity_id)
        if not hasattr(request.user, 'has_row_perm') \
                or not request.user.has_row_perm(station, 'edit'):
            return Response('Forbidden', status=status.HTTP_403_FORBIDDEN)

        return super(TimeseriesList, self).post(request, *args, **kwargs)


class TimeseriesDetail(generics.RetrieveUpdateDestroyAPIView):
    model = models.Timeseries
    permission_classes = (CanEditOrReadOnly,)
