# -*- coding: utf-8 -*-
#!/usr/bin/python

# iWidget application for openmeteo Enhydris software
# This software is provided with the AGPL license
# Copyright (c) 2013-2014 National Techincal University of Athens

from django.core.exceptions import ImproperlyConfigured
from django.conf import settings
from datetime import datetime, timedelta
import json
import urllib2

try:
    getattr(settings, 'REST_API_HOST', '')
except ImproperlyConfigured:
    settings = object()

API_HOST = getattr(settings, 'REST_API_HOST', '195.212.132.10')
API_PORT = getattr(settings, 'REST_API_PORT', '10039')
API_BASE_URL = getattr(settings, 'REST_API_BASE_URL', 'iWidget')
PROXY = getattr(settings, 'REST_API_PROXY', '')

class APIIntegrityError(Exception):
    pass

def _connect_and_get(url_component):
    """
    Connects to the url formed by the global API_* settings and the
    url_component and returns a python response, usually a list or a
    dictionary.
    e.g.:
        ``_connect_and_get('devices')`` will connect to:

    "http://195.212.132.10:10039/iWidget/devices" and will bring a
    list of devices. 

    >>> assert _connect_and_get('devices')
    """
    url = u'http://{0}:{1}/{2}/{3}'.format(API_HOST, API_PORT,
            API_BASE_URL, url_component)
    url = url.replace(' ', '%20')
    if PROXY:
        proxy = urllib2.ProxyHandler({'http': PROXY})
        opener = urllib2.build_opener(proxy)
        urllib2.install_opener(opener)
    response = urllib2.urlopen(url)
    return json.load(response)

def residential_devices():
    """
    Returns a full list of the residential devices. Devices are
    selected by device type="Output". Results are validated so
    customerType is "residential". If this fails that means some
    design has been changed and function should be revalidated.

    >>> devices = residential_devices()
    >>> assert len(devices)>0
    >>> zones = zone_devices()
    >>> # A data integrity test, add this to the script
    >>> zone_ids = [x['id'] for x in zones]
    >>> for device in devices:
    ...     assert device['parent'] in zone_ids
    """
    devices = _connect_and_get('devices/Output')
    for device in devices:
        if device['customerType'] != 'residential':
            raise APIIntegrityError('An output device has '
                    'customerType something else than "residential"')
    return devices

def zone_devices():
    """
    Returns a full list of zones

    >>> zones = zone_devices()
    >>> assert len(zones)>0
    """
    zones = _connect_and_get('devices/Zone')
    for zone in zones:
        if zone['customerType'] != 'Utility':
            raise APIIntegrityError('A zone device has '
                    'customerType something else than "Utility"')
    return zones

DATETIME_MIN = datetime(1970,1,1,0,0,0)
DATETIME_MAX = datetime(2034,1,1,0,0,0)

VALUE_MIN = 0.0
VALUE_MAX = 100000.0

def get_raw_timeseries(device_id, start=DATETIME_MIN,
        end=DATETIME_MAX):
    """
    Retrieves the raw time series data for the ``device_id``.
    If ``start`` and ``end`` specified, gets data for this interval or
    else an attempt to bring the whole time series data is performed.

    If a time series cannot be retrieved then function returns None.

    This function returns a generator object for efficiency. If you
    need a time series list then use list comprehesion like in the
    following doctest. Each item is a two members tuple:
    (timestamp, value)

    If value out of bounds or cannot converted to floating point
    number, then a float('NaN') (NaN stands for Not a Number) is put.

    Timestamps are rounded to the nearest minute

    >>> series = get_raw_timeseries('00060904')
    >>> series = ([record for record in series])
    >>> assert len(series)>1
    """
    url_component = 'timeSeries/{0}/raw?startTime={1}&endTime={2}'.\
            format( str(device_id),
            start.strftime('%Y-%m-%d %H:%M:%S'),
            end.strftime('%Y-%m-%d %H:%M:%S'))
    try:
        series = _connect_and_get(url_component)
    except (urllib2.URLError, urllib2.HTTPError):
        return
    if not len(series) or 'timeSeries' not in series[0]:
        return
    series = series[0]['timeSeries']
    for record in series:
        try:
            value = float(record['value'])
            if value<VALUE_MIN or value>VALUE_MAX:
                value = float('NaN')
        except ValueError:
            value = float('NaN')
        timestamp = datetime.strptime(record['date'],
                '%Y-%m-%d %H:%M:%S')
        if timestamp.second>=30:
            timestamp += timedelta(seconds=60)
        timestamp = timestamp.replace(second=0)
        yield timestamp, value

if __name__ == '__main__':
    import doctest
    doctest.testmod()
