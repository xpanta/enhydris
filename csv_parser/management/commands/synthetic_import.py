__author__ = 'chris'
from django.core.management.base import BaseCommand, CommandError
from ftplib import FTP, all_errors
from fnmatch import fnmatch
from os import path, listdir
from datetime import datetime, timedelta
import logging
from _commonlib import process_data
from iwidget.models import UserValidationKey

def find_nth(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start


def process_file(_filename, _path, force, zone):
    """
    This function just gets the data row by row and creates a list of arrays
    consistent for all different csv files that will comply with the common
    process_data function in commonlib
    :param _filename:
    :param _path:
    :return:
    """
    log = logging.getLogger(__name__)

    def initialize_series():
        return dict(WaterCold=[], Electricity=[])

    with open(path.join(_path, _filename), 'r') as f:
        rows = []
        for line in f:
            rows.append(line)
        usernames = {}
        meter_data = {}
        used_meters = []  # to create a new empty series for each new meter
        for row in rows:
            i = find_nth(row, "|", 3)
            line = row[0:i].split('|')
            meter_id = line[0]
            if meter_id not in used_meters:
                used_meters.append(meter_id)
                series = initialize_series()  # new meter! Init new series!
            _dt = line[1]
            consumption = line[2]
            if not consumption:
                consumption = 0
            consumption = float(consumption)
            _type = "WaterCold"
            dt = datetime.strptime(_dt, "%d-%m-%Y %H:%M:%S")
            #series[_type].append((dt, consumption))
            """
                meter_data = dict of dicts of arrays
            """
            try:  # find previously inserted value
                _dict = meter_data[meter_id]
                _dict[_type].append((dt, consumption))
                #print "append for %s value %s (%s)" % (_type, consumption, dt)
            except KeyError:  # add new meter data
                series[_type].append((dt, consumption))
                meter_data[meter_id] = series
                #print "create for %s value %s (%s)" % (_type, consumption, dt)
                # when we create a HH we need a new username
                usernames[meter_id] = meter_id
        z_names = [zone]
        process_data(meter_data, usernames, force, z_names, {})


class Command(BaseCommand):
    help = 'Command that imports from Synthetic Data files'

    def handle(self, *args, **options):
        log = logging.getLogger(__name__)
        try:
            timer1 = datetime.now()
            log.debug("starting Synthetic Data import. Setting timer at %s" % timer1)
            _path = "data/waterville/"
            new_files = sorted(listdir(_path))
            for _filename in new_files:
                print "reading {x}".format(x=_filename)
                process_file(_filename, _path, True, "Waterville Zone 1")
                timer2 = datetime.now()
                mins = (timer2 - timer1).seconds / 60
                secs = (timer2 - timer1).seconds % 60
                log.debug("process ended. It took %s "
                          "minutes and %s seconds." % (mins, secs))
        except Exception as e:
            raise CommandError(repr(e))
