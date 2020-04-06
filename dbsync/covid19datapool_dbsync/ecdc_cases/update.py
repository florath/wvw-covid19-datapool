'''
Import module handling the data from the
  European Centre for Disease Prevention and Control
Web page

Since beginning of April 2020 they provide data also in csv, json and
xml under a fixed URL.
'''

import datetime
import json
import requests
from google.cloud import firestore

from lib.data_import import DataCollectionImporter
from lib.metadata import update_metadata

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


def update_data(environment, jdata):
    '''Update the data in the database'''
    database = firestore.Client()
    tab_ref = database.collection(
        "covid19datapool/%s/ecdc_cases/data/collection" % environment)
    dci = DataCollectionImporter(tab_ref, "ecdc_cases")
    dci.import_data(jdata, handle_one_data_line)
    dci.remove_old_data()
    update_metadata(database, "ecdc_cases/metadata.json",
                    environment, "ecdc_cases")


def update_data_ecdc_cases(environment, ignore_errors):
    '''Main function to update all ecdc cases'''
    print("update_data_ecdc_cases called [%s] [%s]" %
          (environment, ignore_errors))
    jdata = download_data()
    if jdata is None:
        print("ERROR: cannot download data")
        return
    update_data(environment, jdata['records'])
    print("update_data_ecdc_cases finished")


if __name__ == '__main__':
    # For (local) testing: only update the data
    update_data_ecdc_cases("prod", False)
