'''
Updates / Imports the data from RKI
'''

import datetime
import requests
import json
import pycountry
import re

from google.cloud import firestore

from data_import.lib.utils import import_data_collection, \
    get_available_data_ids, ls, update_metadata, get_metadata_from_db


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
        age_pat = re.compile("A(\d*)\-A(\d*)")
        age_match = age_pat.search(data['Altersgruppe'])
        age_lower = int(age_match.group(1))
        age_upper = int(age_match.group(2))

    nd = {
        'timestamp': data['Meldedatum'] / 1000.0, # given in ms
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
        nd['age-lower'] = age_lower

    if age_upper is not None:
        nd['age-upper'] = age_upper

    if sex is not None:
        nd['sex'] = sex

    # JSON cannot be directly used - because of the JSON is
    # not ordered.
    sha_str = str(data['Meldedatum']) + str(data['AnzahlFall']) \
        + str(data['AnzahlTodesfall']) + str(data['Bundesland']) \
        + str(data['Geschlecht']) + str(data['Altersgruppe']) \
        + str(data['IdBundesland']) + str(data['Landkreis']) \
        + str(data['ObjectId']) + str(data['IdLandkreis'])

    return [(nd, sha_str), ]


DLURL = "https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/RKI_COVID19/FeatureServer/0/query?where=Meldedatum%3D%27{dldate}%27&outFields=*&f=json"

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

        for ds in jdata['features']:
            yield ds

        cur_day += datetime.timedelta(days=1)
        if cur_day >= end_day:
            break


def update_data(db, environment, last_updated):
    '''Update data'''
    tab_ref = db.collection(
        "covid19datapool/%s/rki_cases/data/collection" % environment)
    data_available_ids = get_available_data_ids(tab_ref)
    import_data_collection(generator_rki_data(last_updated), handle_obj_cb,
                           tab_ref, data_available_ids)


def update_data_rki_cases(environment, ignore_errors):
    print("update_data_rki_cases called [%s] [%s]" %
          (environment, ignore_errors))

    db = firestore.Client()
    metadata_from_db = get_metadata_from_db(db, environment, "rki_cases")

    # date --date 2020-01-01 "+%s"
    last_updated = 1577833200
    if metadata_from_db is not None and 'last_updated' in metadata_from_db:
        last_updated = metadata_from_db['last_updated']
    print("INFO: last updated [%d]" % last_updated)

    update_data(db, environment, last_updated)
    update_metadata(db, "rki_cases/metadata.json",
                    environment, "rki_cases")
    print("update_data_rki_cases finished [%s] [%s]" %
          (environment, ignore_errors))


if __name__ == '__main__':
    '''For (local) testing: only update the data'''
    update_data_rki_cases("prod", True)
