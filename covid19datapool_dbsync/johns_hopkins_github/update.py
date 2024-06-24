'''
File which implements the data import of
the Johns Hopkins CSSE data set
'''

import csv
import importlib
import os
import shutil
import tempfile

import dateutil.parser
import git
from lib.data_import import DataCollectionImporter
from lib.parse_args import parse_args_common

GIT_REPO_URL = "https://github.com/CSSEGISandData/COVID-19.git"
DATA_DIR = "csse_covid_19_data/csse_covid_19_daily_reports"
COUNTRY2ISO_MAPPING = "johns_hopkins_github/jh-country2iso.csv"


country2iso = {}
with open(COUNTRY2ISO_MAPPING, newline='') as csvfile:
    content = csv.reader(csvfile, delimiter=',', quotechar='"')
    for line in content:
        country2iso[line[0]] = line[1]


def convert2int(s):
    '''Convert the given string to int. If the string is empty, return 0.'''
    if s == '':
        return 0
    return int(s)


def convert2float(s):
    '''Converts the given string to a Floating-Point Number.
    If the string is empty, return 0.
    This is necessary for longitude and latitude.'''
    if s == '':
        return 0.0
    return float(s)


def convert_ts(ts_str):
    '''A generic date / time converter.

    This is needed because the data set uses (at least) three
    different ways of specifying date / times.'''
    return dateutil.parser.parse(ts_str).timestamp()


def handle_one_data_line_2020_02(line):
    '''Converts one data line into json

    Format of the input data:
    0              1              2           3         4      5
    Province/State,Country/Region,Last Update,Confirmed,Deaths,Recovered,\
       Latitude,Longitude
       6        7
    '''
    try:
        ts = convert_ts(line[2])

        location = [line[1]]
        if line[0] != '':
            location.append(line[0])

        nd = {
            'timestamp': ts,
            'infected_total': convert2int(line[3]),
            'deaths_total': convert2int(line[4]),
            'recovered_total': convert2int(line[5]),
            'source': 'johns_hopkins_github',
            'original': {
                'location': location
            },
            # The 'strip()' is needed because of incorrect input data, e.g.
            # , Azerbaijan,2020-02-28T15:03:26,1,0,0
            'iso-3166-1': country2iso[line[1].strip()],
        }

        if len(line) > 6:
            # Then the longitute and latitude are given
            nd['longitude'] = convert2float(line[6])
            nd['latitude'] = convert2float(line[7])

        sha_str = "".join(line)
        return [(nd, sha_str), ]

    except ValueError as ve:
        # If there is a problem e.g. converting the ts
        # just go on.
        print("ERROR converting [%s]: [%s]" (line, ve))


def handle_unassigned_data(line):
    '''Handles one data line, which has in the Admin2 field a "Unassigned"/
     parameter.
    The Format of the input data is the as in handle_one_data_line_2020_03:
     0       1            2           3                 4         5
    FIPS, Admin2, Province/State, Country/Region, Last Update, Latitude,/
    Longitude, Confirmed, Deaths, Recovered, (Active)
        6          7        8         9
    Active is ignored, because it is not clear what is meant by Active.
    It seems like almost all entries are filled with 0.

    If Admin2 is set to "Unassigned" and it has 0 Death,/
    0 Confirmed and 0 Recovered cases, this line will be ignored.
    '''
    if line[7] and line[8] and line[9] == 0:
        pass
    else:
        try:
            ts = convert_ts(line[4])
            nd = {
                'timestamp': ts,
                'infected_total': convert2int(line[7]),
                'deaths_total': convert2int(line[8]),
                'recovered_total': convert2int(line[9]),
                'source': 'johns_hopkins_github',
                'original': {
                    'location': [line[3], line[2], line[1], line[0]]
                },
                # The 'strip()' is needed because of incorrect input data, e.g.
                # , Azerbaijan,2020-02-28T15:03:26,1,0,0
                'iso-3166-1': country2iso[line[3].strip()],
                # ToDo: fill in missing iso-3166-2 region code
                'longitude': convert2float(line[6]),
                'latitude': convert2float(line[5])
            }

            sha_str = "".join(line)
            return [(nd, sha_str), ]

        except ValueError as ve:
            # If there is a problem e.g. converting the ts
            # just go on.
            print("ERROR converting [%s]: [%s]"(line, ve))


def handle_one_data_line_2020_03(line):
    '''Converts one data line into json

    Format of the input data:
     0       1            2           3                 4         5
    FIPS, Admin2, Province/State, Country/Region, Last Update, Latitude,/
    Longitude, Confirmed, Deaths, Recovered, (Active)
        6          7        8         9

    Active is ignored, because it is not clear what is meant by Active.
    It seems like almost all entries are filled with 0.
    '''

    try:
        ts = convert_ts(line[4])
        if line[2] == 'Unassigned':
            handle_unassigned_data(line)
        else:
            nd = {
                'timestamp': ts,
                'infected_total': convert2int(line[7]),
                'deaths_total': convert2int(line[8]),
                'recovered_total': convert2int(line[9]),
                'source': 'johns_hopkins_github',
                'original': {
                    'location': [line[3], line[2], line[1], line[0]]
                },
                # The 'strip()' is needed because of incorrect input data, e.g.
                # , Azerbaijan,2020-02-28T15:03:26,1,0,0
                'iso-3166-1': country2iso[line[3].strip()],
                # ToDo: fill in missing iso-3166-2 region code
                'longitude': convert2float(line[6]),
                'latitude': convert2float(line[5])
            }

            sha_str = "".join(line)
            return [(nd, sha_str), ]

    except ValueError as ve:
        # If there is a problem e.g. converting the ts
        # just go on.
        print("ERROR converting [%s]: [%s]" (line, ve))


def get_callback_based_on_header(header):
    '''Depending on the header return the appropriate callback function'''

    if header[0][0] == '\ufeff':
        header[0] = header[0][1:]

    if header == ['Province/State', 'Country/Region', 'Last Update',
                  'Confirmed', 'Deaths', 'Recovered']:
        return handle_one_data_line_2020_02
    if header == ['Province/State', 'Country/Region', 'Last Update',
                  'Confirmed', 'Deaths', 'Recovered', 'Latitude', 'Longitude']:
        return handle_one_data_line_2020_02

    if header == ['FIPS', 'Admin2', 'Province_State', 'Country_Region',
                  'Last_Update', 'Lat', 'Long_', 'Confirmed', 'Deaths',
                  'Recovered', 'Active', 'Combined_Key']:
        return handle_one_data_line_2020_03

    print("Unknown header in datafile [%s]" % header)
    return None


def handle_one_data_file(tab_ref, dci, fname):
    with open(fname, newline='') as csvfile:
        content = csv.reader(csvfile, delimiter=',', quotechar='"')
        header = next(content)
        hod_cb = get_callback_based_on_header(header)
        if hod_cb is None:
            print("No callback available for the data file [%s] - skipping"
                  % fname)
            return
        dci.import_data(content, hod_cb)


def update_git(tmp_dir):
    '''Update the git repo

    This is a very first basic implementation which clones the repo every time.
    Later on this can be changed in (just) updating a possible existing one.
    '''
    print("update_git called [%s]" % tmp_dir)
    git.Repo.clone_from(GIT_REPO_URL, tmp_dir, depth=1)
    print("update_git finished [%s]" % tmp_dir)


def update_data(tmp_dir, environment, dbenv):
    '''Reads in the data from the git repo, converts it and
    pushes it into the DB'''
    print("update_data called [%s] [%s]" % (tmp_dir, environment))
    print("update_data creating connection to Firestore")
    dbmod = importlib.import_module("lib.db.%s" % dbenv)
    dbclient = dbmod.DBClient("johns_hopkins_github", environment)
    dbclient.update_metadata("johns_hopkins_github/metadata.json")

    print("update_data handle files")
    dci = DataCollectionImporter(dbclient, "johns_hopkins_github")
    for fname in os.listdir(os.path.join(tmp_dir, DATA_DIR)):
        if fname.endswith(".csv"):
            print("update_data handling file [%s]" % fname)
            handle_one_data_file(dbclient, dci,
                                 os.path.join(tmp_dir, DATA_DIR, fname))
    dci.remove_old_data()
    dbclient.sync()
    print("update_data finished [%s]" % tmp_dir)


def update_dataset(environment, ignore_errors,
                   dbenv="google_firestore"):
    print("import_data_johns_hopkins_github called [%s] [%s]" %
          (environment, ignore_errors))
    try:
        tmp_dir = tempfile.mkdtemp(prefix="johns-hopkins-github", dir="/tmp")
        print("import_data_johns_hopkins_github start [%s]" % tmp_dir)
        update_git(tmp_dir)
        update_data(tmp_dir, environment, dbenv)
        print("import_data_johns_hopkins_github finished [%s]" % tmp_dir)
    except Exception as ex:
        print("import_data_johns_hopkins_github Exception [%s]" % ex)
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)

    # Check for remaining files in /tmp
    print("import_data_johns_hopkins_github finished")


if __name__ == '__main__':
    '''For (local) testing: only update the data'''
    dbenv = parse_args_common()
    update_data("/tmp/jh-covid-19", "prod", dbenv)
