'''
File which implements the data import of
the Johns Hopkins CSSE data set
'''

import csv
import dateutil.parser
import git
import os
import shutil
import hashlib
from google.cloud import firestore
from data_import.lib.utils import import_data_collection, get_available_data_ids


GIT_REPO_URL = "https://github.com/CSSEGISandData/COVID-19.git"
GIT_REPO_LOCAL = "/tmp/jh-covid-19"
DATA_DIR = GIT_REPO_LOCAL + "/csse_covid_19_data/csse_covid_19_daily_reports"
COUNTRY2ISO_MAPPING = "data_import/jh-country2iso.csv"


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
    '''Converts the given string to a Floating-Point Number. If the string is empty, return 0.
    This is necessary for longitude and latitude.'''
    if s == '':
        return 0;
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

    Latitude and Longitude are ignored (as they change from time to time
    even for the same place).  IHMO there are better ways to map the adm
    fields to geographical data.
    '''
    try:
        ts = convert_ts(line[2])

        location = [line[1]]
        if line[0] != '':
            location.append(line[0])

        # The 'strip()' is needed because of incorrect input data, e.g.
        # , Azerbaijan,2020-02-28T15:03:26,1,0,0
        adm = [ country2iso[line[1].strip()], ]

        nd = {
            'timestamp': ts,
            'infected': convert2int(line[3]),
            'deaths': convert2int(line[4]),
            'recovered': convert2int(line[5]),
            'source': 'Johns-Hopkins-github',
            'original': {
                'location': location
            },
            'adm': adm,
        }

        sha_str = str(ts) + line[1] + line[3] + line[4] + line[5]

        return nd, hashlib.sha256(sha_str.encode("utf-8")).hexdigest()

    except ValueError as ve:
        # If there is a problem e.g. converting the ts
        # just go on.
        print("ERROR converting [%s]: [%s]" (line, ve))


def handle_one_data_line_2020_03(line):
    '''Converts one data line into json

    Format of the input data:
     0       1            2           3                 4         5
    FIPS, Admin2, Province/State, Country/Region, Last Update, Latitude,/
    Longitude, Confirmed, Deaths, Recovered, Active
        6          7        8         9        10
    '''

    try:
        ts = convert_ts(line[4])

        location = [line[2]]
        if line[3] != '':
            location.append(line[3])

        # The 'strip()' is needed because of incorrect input data, e.g.
        # , Azerbaijan,2020-02-28T15:03:26,1,0,0
        adm = [country2iso[line[1].strip()], convert2int(line[0]), line[1]]

        nd = {
            'timestamp': ts,
            'latitude': convert2float(line[5]),
            'longitude': convert2float(line[6]),
            'confirmed': convert2int(line[7]),
            'deaths': convert2int(line[8]),
            'recovered': convert2int(line[9]),
            'active': convert2int(line[10]),
            'source': 'Johns-Hopkins-github',
            'original': {
                'location': location
            },
            'adm': adm,
        }

        sha_str = str(ts) + line[1] + line[3] + line[4] + line[5] + line[6] + line[7] + line[8]

        return nd, hashlib.sha256(sha_str.encode("utf-8")).hexdigest()

    except ValueError as ve:
        # If there is a problem e.g. converting the ts
        # just go on.
        print("ERROR converting [%s]: [%s]" (line, ve))


def get_callback_based_on_header(header):
    '''Depending on the header return the appropriate callback function'''

    if header == ['Province/State', 'Country/Region', 'Last Update',
                  'Confirmed', 'Deaths', 'Recovered']:
        return handle_one_data_line_2020_02
    if header == ['\ufeffProvince/State', 'Country/Region', 'Last Update',
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


def handle_one_data_file(tab_ref, data_available_ids, fname):
    with open(fname, newline='') as csvfile:
        content = csv.reader(csvfile, delimiter=',', quotechar='"')
        header = next(content)
        hod_cb = get_callback_based_on_header(header)
        if hod_cb == None:
            print("No callback available for the data file [%s] - skipping" % fname)
            return
        import_data_collection(content, hod_cb, tab_ref, data_available_ids)


def update_git():
    '''Update the git repo

    This is a very first basic implementation which clones the repo every time.
    Later on this can be changed in (just) updating a possible existing one.
    '''
    shutil.rmtree(GIT_REPO_LOCAL, ignore_errors=True)
    repo = git.Repo.clone_from(GIT_REPO_URL, GIT_REPO_LOCAL, depth=1)


def update_data():
    '''Reads in the data from the git repo, converts it and pushes it into the DB'''
    db = firestore.Client()
    tab_ref = db.collection(u"cases")\
                .document("sources")\
                .collection("johns_hopkins_github")

    data_available_ids = get_available_data_ids(tab_ref)
    
    for fname in os.listdir(DATA_DIR):
        if fname.endswith(".csv"):
            handle_one_data_file(tab_ref, data_available_ids, os.path.join(DATA_DIR, fname))

    
def import_data_johns_hopkins_github():
    print("Called import_data_johns_hopkins_github")
    update_git()
    update_data()
    print("Finished import_data_johns_hopkins_github")


if __name__ == '__main__':
    '''For (local) testing: only update the data'''
    update_data()
    
