__author__ = 'chris'
from django.core.management.base import BaseCommand, CommandError
from fnmatch import fnmatch
from os import path, listdir
from datetime import datetime, timedelta
import unicodecsv as csv
import logging
from _commonlib import process_data


def create_15_mins(dt, consumption):
    min_dt = dt.replace(hour=0, minute=15)
    min_dt = min_dt - timedelta(days=1)
    max_dt = dt.replace(hour=0, minute=0)
    dc = consumption / 96.0
    _tuples = []
    while min_dt <= max_dt:
        _tuples.append((min_dt, dc))
        min_dt = min_dt + timedelta(minutes=15)

    return _tuples


def parse_prev_consumption(_filename, _path):
    meter_data = {}
    with open(path.join(_path, _filename), 'r') as f:
        data = csv.reader(f, encoding="utf-8")
        x = 0
        for row in data:
            if x == 0:
                x += 1  # skip first row
                continue
            meter_id = row[0]
            if meter_id:
                consumption = row[2]
                if not consumption:
                    consumption = 0
                consumption = float(consumption)
                """
                    meter_data = dict of dicts of arrays
                """
                try:  # find previously inserted value
                    meter_data[meter_id] += consumption
                except KeyError:  # add new meter data
                    meter_data[meter_id] = consumption
                    # when we create a HH we need a new username
    return meter_data


def process_file(_filename, _path, old_cons):
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
        usernames = {}
        data = csv.reader(f, encoding="utf-8")
        meter_data = {}
        fifteen_data = {}
        x = 0
        used_meters = []  # to create a new empty series for each new meter
        for row in data:
            if x == 0:
                x += 1  # skip first row
                continue
            meter_id = row[0]
            if not meter_id:
                meter_id = row[1]
            if meter_id not in used_meters:
                used_meters.append(meter_id)
                series = initialize_series()  # new meter! Init new series!
            if meter_id:
                _date = row[3]
                _time = row[4]
                consumption = row[2]
                if not consumption:
                    consumption = 0
                consumption = float(consumption)
                try:
                    cons = old_cons[meter_id]
                    consumption -= float(cons)
                    consumption /= 1000.0
                except (KeyError, ValueError) as e:
                    log.debug("UK: Consumption value for meter %s and date %s "
                              "not inserted because %s"
                              % (meter_id, _date, repr(e)))
                    consumption = 0
                _type = "WaterCold"
                _dt = "%s %s" % (_date, _time)
                dt = datetime.strptime(_dt, "%d/%m/%Y %H:%M")
                #series[_type].append((dt, consumption))
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
                    username = "GB" + meter_id
                    usernames[meter_id] = username
        z_name = "UK water"
        process_data(meter_data, usernames, False, z_name)



class Command(BaseCommand):
    help = 'Command that imports from Athens Consumption Data csv file'

    def handle(self, *args, **options):
        log = logging.getLogger(__name__)
        try:
            _curr_user_filename = args[0]
            _prev_user_filename = args[1]
        except IndexError:
            _curr_user_filename = ""
            _prev_user_filename = ""
        try:
            timer1 = datetime.now()
            log.debug("staring UK import. Setting timer at %s" % timer1)
            _curr_file = None
            _prev_file = None
            _path = "data/southern/"
            all_files = sorted(listdir(_path))
            today = datetime.today()
            # I used %02d to format two digits from the datetime object
            _date1 = "%02d_%02d_%s" % (today.day, today.month, today.year)
            _pattern1 = _date1 + "*"
            for f_name in all_files:
                if fnmatch(f_name, _pattern1):
                    _curr_file = f_name
            # Let's find previous metre data file (unfortunately
            # we can't know when was the previous time we had a data file
            # so we need to go back n (=max 15) days.
            found = False
            x = 1
            while not found and x < 15:
                prev = today - timedelta(days=x)
                _date2 = "%02d_%02d_%s" % (prev.day, prev.month,
                                           prev.year)
                _pattern2 = _date2 + "*"
                for f_name in all_files:
                    if fnmatch(f_name, _pattern2):
                        _prev_file = f_name
                        found = True
                x += 1
            _prev_file = "13_10_14.csv"
            _curr_file = "14_10_10_UK.csv"
            if _curr_user_filename:
                _curr_file = _curr_user_filename
            if _prev_user_filename:
                _prev_file = _prev_user_filename
            if _curr_file and _prev_file:
                log.info("parsing file %s" % _curr_file)
                force = False  # True = Rewrite
                old_cons = parse_prev_consumption(_prev_file, _path)
                process_file(_curr_file, _path, old_cons)
                timer2 = datetime.now()
                mins = (timer2 - timer1).seconds / 60
                secs = (timer2 - timer1).seconds % 60
                log.debug("process ended. It took %s "
                          "minutes and %s seconds." % (mins, secs))
            else:
                log.info("No files found for today and yesterday data! "
                         "Stopping!")
        except Exception as e:
            raise CommandError(repr(e))
