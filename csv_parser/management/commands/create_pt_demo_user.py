__author__ = 'Chris Pantazis'
from django.core.management.base import BaseCommand, CommandError
from ftplib import FTP, all_errors
from fnmatch import fnmatch
from os import path, listdir
from datetime import datetime, timedelta
import logging
from _commonlib import process_data

_max = 30


def create_15_mins(dt, consumption):
    _tuples = []
    dt4 = dt - timedelta(minutes=15)
    dt3 = dt - timedelta(minutes=30)
    dt2 = dt - timedelta(minutes=45)
    dt1 = dt - timedelta(minutes=60)
    d_cons = consumption / 4
    _tuples.append((dt1, d_cons))
    _tuples.append((dt2, d_cons))
    _tuples.append((dt3, d_cons))
    _tuples.append((dt4, d_cons))
    return _tuples


def find_nth(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start


def process_file(raw_data, _path, force, z_dict):
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

    z_names = []
    usernames = {}
    meter_data = {}
    used_meters = []  # to create a new empty series for each new meter
    curr_data = {}  # to calculate and store periodic values from total
    for row in raw_data:
        meter_id = row[0]
        consumption = float(row[2])
        _dt = row[1]
        dt = datetime.strptime(_dt, "%d-%m-%Y %H:%M:%S")
        try:
            _dict = curr_data[meter_id]
            _dict[dt] = consumption
        except KeyError:
            _dict = {dt: consumption}
            curr_data[meter_id] = _dict
    # Now we will try and create period values by subtracting
    # the previous value for each consumption value and finally
    # from the last one the yesterday's total (old_cons).
    keys = curr_data.keys()
    for m_id in keys:
        values = curr_data[m_id].keys()
        timestamps = sorted(values)
        _dict = curr_data[m_id]
        for c in range(len(timestamps)-1, 0, -1):  # 0: stops at 1
            val1 = _dict[timestamps[c]]
            val2 = _dict[timestamps[c-1]]
            cons = val1 - val2
            _dict[timestamps[c]] = cons
        _dict[timestamps[0]] = 0  # first recorded consumption will be 0

    for meter_id in keys:
        if meter_id not in used_meters:
            used_meters.append(meter_id)
            series = initialize_series()  # new meter! Init new series!

        timestamps = curr_data[meter_id].keys()
        for ts in timestamps:
            dt = ts
            consumption = curr_data[meter_id][dt]
            if not consumption:
                consumption = 0
            consumption = float(consumption) / 1000.0  # make it cubic metres
            _type = "WaterCold"
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
                username = "PT" + meter_id
                usernames[meter_id] = username
        keys = z_dict.keys()
        for k in keys:
            z = z_dict[k]
            if z not in z_names:
                z_names.append(z)
    process_data(meter_data, usernames, force, z_names, z_dict)


class Command(BaseCommand):
    help = 'Command that imports from AGS Server Consumption Data txt file'

    def handle(self, *args, **options):
        log = logging.getLogger(__name__)
        error = False
        z_dict = {}
        user_filename = None
        custom_date = None
        new_files = []
        try:
            arg = args[0]
            param = arg.split('=')[0]
            value = arg.split('=')[1]
            if param == "file":
                user_filename = value
                new_files = [user_filename]  # files to be imported
            elif param == "date":
                user_filename = None
                custom_date = datetime.strptime(value, "%Y-%m-%d")
                today = custom_date
                target = datetime.today()
                _path = "data/ags/"
                all_files = sorted(listdir(_path))
                while today <= target:
                    _date = "TM%s%02d%02d" % (str(today.year)[2:],
                                              today.month, today.day)
                    _pattern = _date + "*"
                    for f_name in all_files:
                        if fnmatch(f_name, _pattern):
                            new_files.append(f_name)
                    today += timedelta(days=1)
        except IndexError:
            user_filename = ""
            custom_date = ""
            new_files = []  # files to be imported in this session
        try:
            timer1 = datetime.now()
            log.debug("starting AGS Portugal import. Setting timer at %s" % timer1)
            _path = "data/ags/"
            if not user_filename and not custom_date:
                # I used %02d to format two digits from the datetime object
                # Telemetria filename: TM141002_120015.txt
                ## CONNECT TO FTP SERVER AND RETRIEVE FILE LIST
                name = ""
                connection = None
                try:
                    connection = FTP("82.154.251.158")
                    connection.login("IWIDGET01", "oycJSJwc")
                    connection.cwd("telemetria")
                    filenames = connection.nlst()
                    filenames = sorted(filenames)
                    for name in filenames:
                        exists = path.isfile(path.join(_path, name))
                        if not exists:  # fetch it!!
                            new_files.append(name)  # add it to import list
                            localfile = open(path.join(_path, name), 'wb')
                            connection.set_pasv(False)
                            connection.retrbinary("RETR " + name,
                                                  localfile.write, 1024)
                            print "fetched: %s" % name
                        if len(new_files) == _max:
                            break
                except all_errors as e:
                    log.error("Cannot connect to FTP Server because %s" % repr(e))
                    error = True
                    if connection:
                        connection.close()
                    if name:
                        f = path.join(_path, name)
                        import os
                        os.remove(f)

                connection.close()
            if not error:
                raw_data = []
                force = False
                for _filename in new_files:
                    print "reading {x}".format(x=_filename)
                    log.debug("reading {x}".format(x=_filename))
                    # First make on big file concatenating all new downloaded
                    # files.
                    ## "U" for universal-newline mode.
                    my_lines = []
                    with open(path.join(_path, _filename), 'rU') as f:
                        x = 0
                        for line in f:
                            if x == 0:
                                x += 1
                                continue  # skip first line (headers)
                            i = find_nth(line, "|", 3)
                            line = line[0:i]
                            data = line.split('|')
                            username = data[0]
                            if not username == "83924":
                                continue
                            data[0] = "IWDEMO"
                            z = 1
                            z_dict['PT%s' % data[0]] = "Portugal water 1"
                            # Some files are corrupt. Reading stops in
                            # the middle of the line. We keep only the lines
                            # which have meter id, date and consumption values
                            # We drop all others. Pray!
                            if len(data) == 3:
                                raw_data.append(data)

                # Now need to break this raw_data file to smaller ones
                # with timestamps of the same day for each file. This has
                # to be done in this way because I need to know the value of
                # the previous day in order to go on. See _commonlib.py: 296
                day_data = {}
                for row in raw_data:
                    _dt = row[1]
                    _dt = _dt.split(" ")[0]  # pick only the date part
                    try:
                        arr = day_data[_dt]
                        arr.append(row)
                    except KeyError:
                        arr = [row]
                        day_data[_dt] = arr

                # For each date run algorithm:
                dates = sorted(day_data.keys())
                # sort keys by real date not string
                sorted_dates = sorted(dates,
                                      key=lambda a: datetime
                                      .strptime(a, "%d-%m-%Y"))
                for _dt in sorted_dates:
                    print "processing %s" % _dt
                    arr = day_data[_dt]
                    process_file(arr, _path, force, z_dict)
                timer2 = datetime.now()
                mins = (timer2 - timer1).seconds / 60
                secs = (timer2 - timer1).seconds % 60
                log.debug("process ended. It took %s "
                          "minutes and %s seconds." % (mins, secs))
        except Exception as e:
            raise CommandError(repr(e))
