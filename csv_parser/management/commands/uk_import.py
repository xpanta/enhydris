__author__ = 'chris'
from django.core.management.base import BaseCommand, CommandError
from fnmatch import fnmatch
from os import path, listdir
from datetime import datetime, timedelta
import unicodecsv as csv
import logging
from _commonlib import process_data


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
        series = initialize_series()
        x = 0
        for row in data:
            if x == 0:
                x += 1  # skip first row
                continue
            meter_id = row[0]
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
                try:  # find previously inserted value
                    _dict = meter_data[meter_id]
                    _dict[_type].append((dt, consumption))
                except KeyError:  # add new meter data
                    series[_type].append((dt, consumption))
                    meter_data[meter_id] = series
                    # when we create a HH we need a new username
                    username = "UK" + meter_id
                    usernames[meter_id] = username
        z_name = "UK electric-water"
        #process_data(meter_data, usernames, force, z_name)


class Command(BaseCommand):
    help = 'Command that imports from Athens Consumption Data csv file'

    def handle(self, *args, **options):
        log = logging.getLogger(__name__)
        try:
            timer1 = datetime.now()
            log.debug("staring UK import. Setting timer at %s" % timer1)
            _filename1 = None
            _filename2 = None
            _path = "data/southern/"
            all_files = sorted(listdir(_path))
            today = datetime.today()
            yesterday = today - timedelta(days=1)
            # I used %02d to format two digits from the datetime object
            _date1 = "%02d_%02d_%s" % (today.day, today.month, today.year)
            _date2 = "%02d_%02d_%s" % (yesterday.day, yesterday.month,
                                       yesterday.year)
            _pattern1 = _date1 + "*"
            _pattern2 = _date2 + "*"
            for f_name in all_files:
                if fnmatch(f_name, _pattern1):
                    _filename1 = f_name
                if fnmatch(f_name, _pattern2):
                    _filename2 = f_name

            if _filename1 and _filename2:
                log.info("parsing file %s" % _filename1)
                force = False  # True = Rewrite
                old_cons = parse_prev_consumption(_filename2, _path)
                process_file(_filename1, _path, old_cons)
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
__author__ = 'chris'
