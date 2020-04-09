'''
Import module handling the data from the
  European Centre for Disease Prevention and Control
Web page

Since beginning of April 2020 they provide data also in csv, json and
xml under a fixed URL.
'''

import datetime
import importlib
import json
import requests

from lib.data_import import DataCollectionImporter
from lib.parse_args import parse_args_common


DOWNLOAD_URL = "https://opendata.ecdc.europa.eu/covid19/casedistribution/json"


def download_data():
    '''Download the JSON data, parse and return it'''
    data_file = requests.get(DOWNLOAD_URL)
    if not data_file.ok:
        return None
    return json.loads(data_file.content)


def handle_one_data_line(line):
    '''Converts one ECDC JSON object to a standard one'''
    timestamp = datetime.datetime(year=int(line['year']),
                                  month=int(line['month']),
                                  day=int(line['day'])).timestamp()

    new_data = {
        'timestamp': timestamp,
        'infected_new': int(line['cases']),
        'deaths_new': int(line['deaths']),
        'source': 'ecdc_cases',
        'original': {
            'location': line['countriesAndTerritories']
        },
        'iso-3166-1': line['geoId']
    }

    sha_str = str(timestamp) + line['cases'] + line['deaths'] + line['geoId']
    return [(new_data, sha_str), ]


def update_data(environment, jdata, db_env):
    '''Update the data in the database'''
    dbmod = importlib.import_module("lib.db.%s" % db_env)
    dbclient = dbmod.DBClient("ecdc_cases", environment)

    dci = DataCollectionImporter(dbclient, "ecdc_cases")
    dci.import_data(jdata, handle_one_data_line)
    dci.remove_old_data()
    dbclient.update_metadata("ecdc_cases/metadata.json")
    dbclient.sync()


def update_data_ecdc_cases(environment, ignore_errors,
                           db_env="google_firestore"):
    '''Main function to update all ecdc cases'''
    print("update_data_ecdc_cases called [%s] [%s]" %
          (environment, ignore_errors))
    jdata = download_data()
    if jdata is None:
        print("ERROR: cannot download data")
        return
    update_data(environment, jdata['records'], db_env)
    print("update_data_ecdc_cases finished")


if __name__ == '__main__':
    # For (local) testing: only update the data
    # (The problem pylint reports does obviously not exists???)
    # pylint: disable=invalid-name
    dbenv = parse_args_common()
    update_data_ecdc_cases("prod", False, dbenv)
