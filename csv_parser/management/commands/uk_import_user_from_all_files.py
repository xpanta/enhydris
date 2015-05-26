__author__ = 'Chris Pantazis'
from django.core.management.base import BaseCommand, CommandError
from fnmatch import fnmatch
from os import path, listdir
from datetime import datetime, timedelta
import unicodecsv as csv
import logging
from _commonlib import process_data


def notify_admins():
    from django.core.mail import EmailMessage
    subject = "iWIDGET: Missing Data File!"
    to = ["xpanta@gmail.com"]
    from_email = 'no-reply@iwidget.up-ltd.co.uk'
    message = "Missing Data File for UK"
    msg = EmailMessage(subject, message, to=to, from_email=from_email)
    msg.send()


def create_15_mins(dt, consumption):
    min_dt = dt.replace(hour=0, minute=0)
    # min_dt = min_dt - timedelta(days=1)
    max_dt = dt.replace(hour=23, minute=45)
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


def process_file(_filename, _path, old_cons, uid):
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
            if meter_id != uid:
                continue
            if not meter_id:
                meter_id = row[1]
            if meter_id not in used_meters:
                used_meters.append(meter_id)
                series = initialize_series()  # new meter! Init new series!
            if meter_id:
                _date = row[3]
                try:
                    _time = row[4]
                except IndexError:
                    _time = "14:05"
                consumption = row[2]
                if not consumption:
                    consumption = 0
                consumption = float(consumption)
                if consumption > 99999999:
                    continue  # probably false reading
                try:
                    cons = old_cons[meter_id]
                    consumption -= float(cons)
                    consumption /= 100.0  # to get litres
                    consumption /= 1000.0  # to get m3
                except (KeyError, ValueError) as e:
                    log.debug("UK: Consumption value for meter %s and date %s "
                              "not inserted because %s"
                              % (meter_id, _date, repr(e)))
                    consumption = 0
                _type = "WaterCold"
                _dt = "%s %s" % (_date, _time)
                try:
                    dt = datetime.strptime(_dt, "%d/%m/%Y %H:%M")
                except ValueError:
                    dt = datetime.strptime(_dt, "%m/%d/%Y %H:%M")

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
        z_names = ["UK water"]
        print "processing %s data" % len(meter_data)
        process_data(meter_data, usernames, False, z_names, {})


class Command(BaseCommand):
    help = 'Command that imports from Athens Consumption Data csv file'

    def handle(self, *args, **options):
        log = logging.getLogger(__name__)
        try:
            uid = args[0]
        except IndexError:
            return -1
        try:
            timer1 = datetime.now()
            log.debug("staring UK import. Setting timer at %s" % timer1)
            _curr_file = None
            _prev_file = None
            _path = "data/southern/"
            # all_files = sorted(listdir(_path))
            # correct_list = []
            # aday = datetime.today()
            # start = aday.replace(day=01, month=10, year=2014)
            # end = aday
            # while start <= end:
            #     _date1 = "%02d_%02d_%s" % (start.day, start.month, str(start.year)[2:])
            #     _pattern1 = _date1 + "*"
            #     _date2 = "%02d_%02d_%s" % (start.day, start.month, str(start.year))
            #     _pattern2 = _date2 + "*"
            #     for f_name in all_files:
            #         if fnmatch(f_name, _pattern1) or fnmatch(f_name, _pattern2):
            #             correct_list.append(f_name)
            #     start += timedelta(days=1)
            correct_list = ['01_10_2014.csv', '06_10_2014_UK.csv', '07_10_2014_UK.csv', '08_10_14_UK.csv', '09_10_2014_UK.csv', '10_10_14_UK.csv', '13_10_14.csv', '15_10_14_UK.csv', '16_10_14_UK.csv', '20_10_14_UK.csv', '21_10_14_UK.csv', '22_10_14_UK.csv', '23_10_14_UK.csv', '24_10_14_UK.csv', '27_10_14_UK.csv', '27_10_2014.csv', '28_10_14_UK.csv', '29_10_14_UK.csv', '30_10_14_UK.csv', '30_10_2014_UK.csv', '03_11_2014_UK.csv', '04_11_14_uk.csv', '05_11_14_UK.csv', '06_11_2014_UK.csv', '10_11_14_uk.csv', '11_11_14_uk.csv', '12_11_14_uk.csv', '13_11_14_uk.csv', '14_11_14_uk.csv', '17_11_14_uk.csv', '19_11_14_uk.csv', '20_11_14_uk.csv', '21_11_14_uk.csv', '24_11_14_uk.csv', '25_11_14_uk.csv', '26_11_14_uk.csv', '27_11_14_uk.csv', '28_11_14_uk.csv', '01_12_14_uk.csv', '02_12_14_uk.csv', '03_12_14_uk.csv', '04_12_14_uk.csv', '05_12_14_uk.csv', '08_12_14_uk.csv', '09_12_14_uk.csv', '10_12_14_uk.csv', '11_12_14_uk.csv', '12_12_14_uk.csv', '15_12_14_uk.csv', '16_12_14_uk.csv', '17_12_14_uk.csv', '18_12_14_uk.csv', '19_12_14_uk.csv', '22_12_14_uk.csv', '05_01_15_uk.csv', '06_01_15_uk.csv', '07_01_15_uk.csv', '08_01_15_uk.csv', '09_01_15_uk.csv', '12_01_15_uk.csv', '13_01_15_uk.csv', '14_01_15_uk.csv', '15_01_15_uk.csv', '16_01_15_uk.csv', '20_01_2015_uk.csv', '21_01_15_uk.csv', '22_01_15_uk.csv', '23_01_15_uk.csv', '26_01_15_uk.csv', '27_01_15_uk.csv', '28_01_15_uk.csv', '29_01_15_uk.csv', '30_01_15_uk.csv', '03_02_15_uk.csv', '05_02_15_uk.csv', '06_02_15_uk.csv', '09_02_15_uk.csv', '10_02_15_uk.csv', '11_02_15_uk.csv', '13_02_15_uk.csv', '16_02_15_uk.csv', '17_02_15_uk.csv', '19_02_15_uk.csv', '20_02_15_uk.csv', '23_02_15_uk.csv', '25_02_15_uk.csv', '26_02_15_uk.csv', '27_02_15_uk.csv', '02_03_15_uk.csv', '03_03_15_uk.csv', '04_03_15_uk.csv', '05_03_15_uk.csv', '06_03_15_uk.csv', '09_03_2015_uk.csv', '10_03_15_uk.csv', '11_03_15_uk.csv', '12_03_15_uk.csv', '13_03_15_uk.csv', '16_03_15_uk.csv', '18_03_15_uk.csv', '19_03_15_uk.csv', '20_03_15_uk.csv', '23_03_15_uk.csv', '25_03_15_uk.csv', '26_03_15_uk.csv', '27_03_2015_uk.csv', '30_03_15_uk.csv', '01_04_15_uk.csv', '02_04_15_uk.csv', '08_04_15.csv', '13_04_15_uk.csv', '14_04_15_uk.csv', '15_04_15_uk.csv', '16_04_15_uk.csv', '17_04_15_uk.csv', '20_04_15_uk.csv', '22_04_15_uk.csv', '23_04_15_uk.csv', '28_04_15_uk.csv', '29_04_15_uk.csv', '30_04_15_uk.csv', '01_05_15_uk.csv']
            for i in range(1, len(correct_list)):
                _curr_file = correct_list[i]
                _prev_file = correct_list[i-1]
                print "importing %s -> %s" % (_prev_file, _curr_file)
                if _curr_file and _prev_file:
                    log.info("parsing file %s" % _curr_file)
                    force = False  # True = Rewrite
                    old_cons = parse_prev_consumption(_prev_file, _path)
                    process_file(_curr_file, _path, old_cons, uid)
                else:
                    log.info("No files found for today and yesterday data! ")
                    continue
            timer2 = datetime.now()
            mins = (timer2 - timer1).seconds / 60
            secs = (timer2 - timer1).seconds % 60
            log.debug("process ended. It took %s "
                      "minutes and %s seconds." % (mins, secs))
        except Exception as e:
            raise CommandError(repr(e))

