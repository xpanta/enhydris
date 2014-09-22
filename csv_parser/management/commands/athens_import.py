__author__ = 'chris'
from django.core.management.base import BaseCommand, CommandError
from fnmatch import fnmatch
from os import path, listdir
from datetime import datetime
import unicodecsv as csv
import logging
from _commonlib import process_data


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

    with open(path.join(_path, _filename), 'r') as f:
        usernames = {}
        data = csv.reader(f, encoding="utf-8")
        meter_data = {}
        series = initialize_series()
        for row in data:
            meter_id = row[0]
            _dt = row[1]
            consumption = row[3]
            if not consumption:
                consumption = 0
            consumption = float(consumption)
            if 'Electricity' in meter_id:
                _type = "Electricity"
            elif 'Water' in meter_id:
                _type = "WaterCold"
            else:
                log.debug("Consumption type not found! Skipping this row!")
                continue
            dt = datetime.strptime(_dt, "%Y/%m/%d %H:%M")
            #series[_type].append((dt, consumption))
            """
                meter_data = dict of dicts of arrays
            """
            beg = meter_id.rfind("_") + 1
            end = meter_id.rfind("/")
            serial_no = meter_id[beg:end]
            try:  # find previously inserted value
                _dict = meter_data[serial_no]
                _dict[_type].append((dt, consumption))
            except KeyError:  # add new meter data
                series[_type].append((dt, consumption))
                meter_data[serial_no] = series
                # when we create a HH we need a new username
                username = serial_no
                usernames[serial_no] = username
                name = "Greece electric-water"
        process_data(meter_data, usernames, force, name)


class Command(BaseCommand):
    help = 'Command that imports from Athens Consumption Data csv file'

    def handle(self, *args, **options):
        log = logging.getLogger(__name__)
        try:
            timer1 = datetime.now()
            log.debug("staring athens import. Setting timer at %s" % timer1)
            _filename = ""
            _path = "data/athens/"
            all_files = listdir(_path)
            today = datetime.today()
            # I used %02d to format two digits from the datetime object
            _date = "%s%02d%02d" % (today.year, today.month, today.day)
            _pattern = _date + "*"
            for f_name in all_files:
                if fnmatch(f_name, _pattern):
                    _filename = f_name
                    break
            if _filename:
                force = False  # True = Rewrite
                process_file(_filename, _path, force)
                timer2 = datetime.now()
                mins = (timer2 - timer1).seconds / 60
                secs = (timer2 - timer1).seconds % 60
                log.debug("process ended. It took %s "
                          "minutes and %s seconds." % (mins, secs))
            else:
                log.debug("No file name found for Athens. Stopping!")
        except Exception as e:
            raise CommandError(repr(e))
