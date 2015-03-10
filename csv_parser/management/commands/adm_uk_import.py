__author__ = 'chris'
from django.core.management.base import BaseCommand, CommandError
from fnmatch import fnmatch
from os import path, listdir
from datetime import datetime, timedelta
import unicodecsv as csv
import logging
from _commonlib import process_data


def create_15_mins(dt, consumption):
    _tuples = []
    dt1 = dt - timedelta(minutes=15)
    d_cons = consumption / 2
    _tuples.append((dt1, d_cons))
    _tuples.append((dt, d_cons))
    return _tuples


def process_file(_filename, _path, force):
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

    ## "U" for universal-newline mode.
    with open(path.join(_path, _filename), 'rU') as f:
        usernames = {}
        data = csv.reader(f, encoding="utf-8")
        meter_data = {}
        used_meters = []  # to create a new empty series for each new meter
        x = 0
        for row in data:
            if x == 0:
                x += 1  # skip first row
                continue
            meter_id = row[0]
            if meter_id not in used_meters:
                used_meters.append(meter_id)
                series = initialize_series()  # new meter! Init new series!
            _dt = row[1]
            _tm = row[2]
            consumption = row[3]
            if not consumption:
                consumption = 0
            consumption = float(consumption)
            _type = "WaterCold"
            str_dt = "%s %s" % (_dt, _tm)
            dt = datetime.strptime(str_dt, "%d/%m/%Y %H:%M")
            """
                meter_data = dict of dicts of arrays
            """
            try:
                _dict = meter_data[meter_id]
                _tuples = create_15_mins(dt, consumption)
                for t in _tuples:
                    _dict[_type].append(t)
            except KeyError:  # add new meter data
                _tuples = create_15_mins(dt, consumption)
                for t in _tuples:
                    series[_type].append(t)
                meter_data[meter_id] = series
                # when we create a HH we need a new username
                username = "GBA" + meter_id
                usernames[meter_id] = username
        z_names = ["UK water"]
        process_data(meter_data, usernames, force, z_names, {})


class Command(BaseCommand):
    help = 'Command that imports from UK ADM Loggers Consumption Data csv file'

    def handle(self, *args, **options):
        log = logging.getLogger(__name__)
        try:
            user_filename = args[0]
        except IndexError:
            user_filename = ""
        try:
            timer1 = datetime.now()
            log.debug("staring ADM UK import. Setting timer at %s" % timer1)
            _filenames = []
            _path = "data/southern/ADM/"
            all_files = sorted(listdir(_path))
            today = datetime.today()
            # I used %02d to format two digits from the datetime object
            _date = "%s%02d%02d" % (today.year, today.month, today.day)
            _pattern = _date + "*"
            for f_name in all_files:
                if fnmatch(f_name, _pattern):
                    _filenames.append(f_name)
            if user_filename:
                _filenames = [user_filename]
            for _filename in _filenames:
                log.info("parsing file %s" % _filename)
                force = False  # True = Rewrite
                process_file(_filename, _path, force)
                timer2 = datetime.now()
                mins = (timer2 - timer1).seconds / 60
                secs = (timer2 - timer1).seconds % 60
                log.debug("process ended. It took %s "
                          "minutes and %s seconds." % (mins, secs))
        except Exception as e:
            raise CommandError(repr(e))
