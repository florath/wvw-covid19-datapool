'''
Updates / Imports the data from RKI
'''

import datetime
import importlib
import json
import re
import requests
import pycountry

from lib.data_import import DataCollectionImporter
from lib.parse_args import parse_args_common


# Need to prepare this - as there is no funtion to
# search for this.
DE_REG_MAPPING = {}
for sd in pycountry.subdivisions:
    if sd.country_code == 'DE':
        DE_REG_MAPPING[sd.name] = sd.code[3:]


def handle_obj_cb(jobj):
    '''Handle / convert one data row

    The input object is JSON with the following structure:
      {
        "IdBundesland": 3,
        "Bundesland": "Niedersachsen",
        "Landkreis": "LK Stade",
        "Altersgruppe": "A35-A59",
        "Geschlecht": "W",
        "AnzahlFall": 1,
        "AnzahlTodesfall": 0,
        "ObjectId": 466277,
        "Meldedatum": 1583971200000,
        "IdLandkreis": "03359",
        "Datenstand": "29.03.2020 00:00",
        "NeuerFall": 0,
        "NeuerTodesfall": -9
      }

    NeuerTodesfall and NeuerFall are ignored as they
    can be extracted from the other available data.
    '''
    data = jobj['attributes']

    sex_map = {
        'M': 'm',
        'W': 'f',
        'unbekannt': None
    }

    assert data['Geschlecht'] in sex_map.keys()
    sex = sex_map[data['Geschlecht']]

    if data['Altersgruppe'] == 'unbekannt':
        age_lower = None
        age_upper = None
    elif data['Altersgruppe'] == 'A80+':
        age_lower = 80
        age_upper = None
    else:
        # This line gives a false positive:
        #  W605 invalid escape sequence '\d'
        # pylint: disable=anomalous-backslash-in-string
        age_pat = re.compile('A(\d*)\-A(\d*)')  # noqa: W605
        age_match = age_pat.search(data['Altersgruppe'])
        age_lower = int(age_match.group(1))
        age_upper = int(age_match.group(2))

    new_data = {
        'timestamp': data['Meldedatum'] / 1000.0,  # given in ms
        'infected': data['AnzahlFall'],
        'deaths': data['AnzahlTodesfall'],
        'iso-3166-1': 'DE',
        'iso-3166-2': DE_REG_MAPPING[data['Bundesland']],
        'original': {
            'IdBundesland': data['IdBundesland'],
            'Landkreis': data['Landkreis'],
            'ObjectId': data['ObjectId'],
            'IdLandkreis': data['IdLandkreis'],
        }
    }

    if age_lower is not None:
        new_data['age-lower'] = age_lower

    if age_upper is not None:
        new_data['age-upper'] = age_upper

    if sex is not None:
        new_data['sex'] = sex

    # JSON cannot be directly used - because of the JSON is
    # not ordered.
    sha_str = str(data['Meldedatum']) + str(data['AnzahlFall']) \
        + str(data['AnzahlTodesfall']) + str(data['Bundesland']) \
        + str(data['Geschlecht']) + str(data['Altersgruppe']) \
        + str(data['IdBundesland']) + str(data['Landkreis']) \
        + str(data['ObjectId']) + str(data['IdLandkreis'])

    return [(new_data, sha_str), ]


DLURL = "https://services7.arcgis.com/mOBPykOjAyBO2ZKk/" \
    "arcgis/rest/services/RKI_COVID19/FeatureServer/0/" \
    "query?where=Meldedatum%3D%27{dldate}%27&outFields=*&f=json"


def generator_rki_data(last_updated):
    '''Generator which returns the data piece by piece

    This reads the input data chunk by chunk and directly passes
    it to the db.  So there is no need for big buffers.
    '''
    print("generator_rki_data last_updated [%s]" % last_updated)
    cur_day = datetime.datetime.fromtimestamp(last_updated)
    # Have a one day overlap - to be sure not to miss any data
    cur_day -= datetime.timedelta(days=1)
    print("generator_rki_data cur_day [%s]" % cur_day)
    # Same here: depending on the update time and the
    # local time zone, check also tomorrows data.
    end_day = datetime.datetime.now() + datetime.timedelta(days=1)
    print("generator_rki_data end_day [%s]" % end_day)

    while True:
        print("generator_rki_data loop for cur_day [%s]" % cur_day)
        url = DLURL.format(dldate=cur_day.strftime("%Y-%m-%d"))
        resp = requests.get(url)

        if not resp.ok:
            print("ERROR: problem during downloading file [%s]" % resp)
            continue

        jdata = json.loads(resp.content)

        for data_set in jdata['features']:
            yield data_set

        cur_day += datetime.timedelta(days=1)
        if cur_day >= end_day:
            break


def update_data(dbclient, last_updated):
    '''Update data'''
    dci = DataCollectionImporter(dbclient, "rki_cases")
    dci.import_data(generator_rki_data(last_updated), handle_obj_cb)
    dci.remove_old_data()


def update_dataset(environment, ignore_errors,
                   dbenv="google_firestore"):
    '''Update the RKI dataset'''
    print("update_data_rki_cases called [%s] [%s]" %
          (environment, ignore_errors))

    print("update_data_rki_cases importing database backend [%s]"
          % dbenv)
    dbmod = importlib.import_module("lib.db.%s" % dbenv)
    dbclient = dbmod.DBClient("rki_cases", environment)
    dbclient.update_metadata("rki_cases/metadata.json")

    # date --date 2020-01-01 "+%s"
    last_updated = 1577833200
    print("INFO: last updated [%d]" % last_updated)

    update_data(dbclient, last_updated)
    print("update_data_rki_cases finished [%s] [%s]" %
          (environment, ignore_errors))
    dbclient.sync()


def main_test():
    '''Test function called when main is called

    For (local) testing: only update the data'''
    dbenv = parse_args_common()
    update_dataset("prod", True, dbenv)


if __name__ == '__main__':
    main_test()
