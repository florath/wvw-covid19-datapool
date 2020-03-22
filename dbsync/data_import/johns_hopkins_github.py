'''
File which imlements the data import of
the Johns Hopkins CSSE data set
'''

import csv
import dateutil.parser
import git
import os
import shutil


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

def convert_ts(ts_str):
    '''A generic date / time converter.

    This is needed because the data set uses (at least) three
    different ways of specifying date / times.'''
    return dateutil.parser.parse(ts_str).timestamp()


def handle_one_data_line(line):
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
            'date': ts,
            'infected': convert2int(line[3]),
            'deaths': convert2int(line[4]),
            'recovered': convert2int(line[5]),
            'source': 'Johns-Hopkins-github',
            'original': {
                'location': location
            },
            'adm': adm,
        }
        print(nd)
        # data.append(nd)
    except ValueError as ve:
        # If there is a problem e.g. converting the ts
        # just go on.
        print("ERROR converting [%s]: [%s]" (line, ve))


def handle_one_data_file(fname):
    with open(fname, newline='') as csvfile:
        try:
            content = csv.reader(csvfile, delimiter=',', quotechar='"')
            # Skip header
            next(content)
            for line in content:
                handle_one_data_line(line)
        except StopIteration as si:
            print("ERROR: StopIteration error in file [%s]" % fname)


def update_git():
    '''Update the git repo

    This is a very first basic implementation which clones the repo every time.
    Later on this can be changed in (just) updating a possible existing one.
    '''
    shutil.rmtree(GIT_REPO_LOCAL, ignore_errors=True)
    repo = git.Repo.clone_from(GIT_REPO_URL, GIT_REPO_LOCAL, depth=1)


def update_data():
    '''Reads in the data from the git repo, converts it and pushes it into the DB'''
    for fname in os.listdir(DATA_DIR):
        if fname.endswith(".csv"):
            handle_one_data_file(os.path.join(DATA_DIR, fname))

    
def import_data_johns_hopkins_github():
    update_git()
    update_data()
    print("Called update_data_johns_hopkins_github")


if __name__ == '__main__':
    '''For (local) testing: only update the data'''
    update_data()
    
