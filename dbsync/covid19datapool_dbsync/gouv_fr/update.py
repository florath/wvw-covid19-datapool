'''
Import the files from the French gouvernement
'''

import csv
import io
import requests
import json
import hashlib
import re
from html.parser import HTMLParser
import dateutil.parser
import importlib

from lib.data_import import DataCollectionImporter


URL_HTML_PAGE = "https://www.data.gouv.fr/" \
    "en/datasets/donnees-relatives-a-lepidemie-du-covid-19"


class GouvFrHTMLParser(HTMLParser):

    def __init__(self):
        super(GouvFrHTMLParser, self).__init__()
        self.__script_tag_found = False
        self.__script = None

    def handle_starttag(self, tag, attrs):
        #print("Encountered a start tag:", tag)
        if tag == 'script' and self.__script == None:
            self.__script_tag_found = True

    def handle_endtag(self, tag):
        #print("Encountered an end tag :", tag)
        if tag == 'script':
            self.__script_tag_found = False

    def handle_data(self, data):
        if self.__script_tag_found:
            self.__script = data

    def get_script_data(self):
        return self.__script


age_group_lower = {
    'A': 0,
    'B': 15,
    'C': 45,
    'D': 65,
    'E': 75
}

age_group_upper = {
    'A': 14,
    'B': 44,
    'C': 64,
    'D': 74
}

# erv - emergency room visits
# cs - covid19 suspicious
def create_dataset(line, sex, i_erv_cs, i_erv, i_hosp,
                   i_sos_med_act_cs, i_sos_med_act):
    '''Create a dataset (total, male, female) from the given
    indices'''

    # It does not make sense to have datasets in the db
    # with no statistics data, check if one is set.
    statistics_data_set = False

    ts = dateutil.parser.parse(line[1]).timestamp()

    ds = {
        'iso-3166-1': "FR",
        'iso-3166-2': str(line[0]),
        'timestamp': ts
    }
    sha = str(line[0]) + str(ts)

    if line[2] in age_group_lower:
        ds['age-lower'] = age_group_lower[line[2]]
        sha += line[2]
    if line[2] in age_group_upper:
        ds['age-upper'] = age_group_upper[line[2]]
        sha += line[2]
    if sex is not None:
        ds['sex'] = sex
        sha += sex

    if i_erv_cs is not None and line[i_erv_cs] != '':
        ds['emergeny-room-visits-covid19-suspicious'] \
            = int(line[i_erv_cs])
        sha += line[i_erv_cs]
        statistics_data_set = True
    if i_erv is not None and line[i_erv] != '':
        ds['emergeny-room-visits'] = int(line[i_erv])
        sha += line[i_erv]
        statistics_data_set = True
    if i_hosp is not None and line[i_hosp] != '':
        ds['hospitalizations-covid19-suspicious'] \
            = int(line[i_hosp])
        sha += line[i_hosp]
        statistics_data_set = True
    if i_sos_med_act_cs is not None and line[i_sos_med_act_cs] != '':
        ds['sos-medical-act-covid19-suspicious'] \
            = int(line[i_sos_med_act_cs])
        sha += line[i_sos_med_act_cs]
        statistics_data_set = True
    if i_sos_med_act is not None and line[i_sos_med_act] != '':
        ds['sos-medical-act'] = int(line[i_sos_med_act])
        sha += line[i_sos_med_act]
        statistics_data_set = True

    if not statistics_data_set:
        return None, None

    return ds, sha


def handle_gouv_fr_departement_emergency_room_visits(line):
    '''Converts one line of departement data into JSON

    0: departement
    1: date of notice
    2: Age group
    3: Number of emergency room visits for suspicion of COVID-19
    4: Total amount of emergency room visits
    5: Number of hospitalizations among emergency department visits
       for suspicion of COVID-19
    6: Number of emergency room visits for suspicion of COVID-19 -
       Males
    7: Number of emergency room visits for suspicion of COVID-19 -
       Females
    8: Total amount of emergency room visits - Males
    9: Total amount of emergency room visits - Females
    10: Number of hospitalizations among emergency department visits
       for suspicion of COVID-19 - Males
    11: Number of hospitalizations among emergency department visits
       for suspicion of COVID-19 - Females
    12: Number of medical acts (SOS Médecin) for suspicion of COVID-19
    13: Total amount of medical acts (SOS Médecin)
    14: Number of medical acts (SOS Médecin) for suspicion of COVID-19
       - Males
    15: Number of medical acts (SOS Médecin) for suspicion of COVID-19
       - Females
    16: Total amount of medical acts (SOS Médecin) - Males
    17: Total amount of medical acts (SOS Médecin) - Females

    WHO DID THIS?!?!?!?! IMPOSSIBLE TO HAVE THIS IN ONE TABLE!!!!
    '''

    assert len(line) == 18
    ds_total, sha_total = create_dataset(line, None, 3, 4, 5, 12, 13)
    ds_male, sha_male = create_dataset(line, "m", 6, 8, 10, 14, 16)
    ds_female, sha_female = create_dataset(line, "f", 7, 9, 11, 15, 17)

    res = []
    if ds_total is not None:
        res.append((ds_total, sha_total))
    if ds_male is not None:
        res.append((ds_male, sha_male))
    if ds_female is not None:
        res.append((ds_female, sha_female))

    return res

def not_implemented():
    assert False


# These are the data which are needed for handling the different
# files.
# For each data set there is given:
# 0: the name of the dataset as it is used in the DB
# 1: a regular expression which matches the data file name
# 2: the callback which handles the data
DATA_MAPPING = [
    [ 'gouv_fr_covid19_emergency_room_visits',
      re.compile('sursaud-covid19-quotidien.*-departement.csv'),
      handle_gouv_fr_departement_emergency_room_visits],
    [ 'gouv_fr_covid19_daily_region',
      re.compile('sursaud-covid19-quotidien.*-region.csv'),
      # TODO!
      None],
    [ 'gouv_fr_covid19_daily_departement',
      re.compile('sursaud-covid19-quotidien.*-france.csv'),
      # TODO!
      None],
    [ 'gouv_fr_covid19_weekly',
      re.compile('sursaud-covid19-hebdomadaire.*'),
      # TODO!
      None],
    # The following is the description (metadata) of the
    # data itself. This is not statistical data and
    # implemented into the source code (used for mapping).
    [ None,
      re.compile('metadonnees-donnees-hospitalieres-covid19.*'),
      None ],
    [ None,
      re.compile('metadonnees-services-hospitaliers-covid19.csv'),
      None ],
    [ None,
      re.compile('metadonnee-urgenceshos-sosmedecins-covid19-quot-dep.csv'),
      None ],
    [ None,
      re.compile('metadonnee-urgenceshos-sosmedecin-covid19-quot-reg.csv'),
      None ],
    [ None,
      re.compile('metadonnee-urgenceshos-sosmedecin-covid19-quot-fra.csv'),
      None ],
    [ None,
      re.compile('metadonnee-urgenceshos-sosmedecins-covid19-hebdo.csv'),
      None ],
    [ None,
      re.compile('code-tranches-dage.csv'),
      None ],
]


def match_filename(fname):
    '''Uses the data mapping table to get the correct entry'''
    print("DEBUG: looking for filename [%s]" % fname)
    for dm in DATA_MAPPING:
        if dm[1].match(fname):
            return dm
    print("ERROR: Filename does not match [%s]" % fname)
    return None


def download_master_html():
    '''Download the main html page

    The master page is the HTML page that contains links to all data
    files. This is needed as this seams to be the only source of
    the filenames.
    '''
    html_file = requests.get(URL_HTML_PAGE)
    parser = GouvFrHTMLParser()
    parser.feed(html_file.text)
    jdata = json.loads(parser.get_script_data())

    datalist = []
    for dist in jdata['distribution']:
        if dist['@type'] != 'DataDownload':
            print("WARNING: distribution entry which is not a "
                  "download [%s]" % dist)
            continue

        data_map = match_filename(dist['name'])
        if data_map is None:
            print("ERROR: No handler for the file [%s] is available"
                  % dist['name'])
            continue
        if data_map[0] is None:
            print("INFO: skipping metadata file [%s]" % dist['name'])
            continue
        datalist.append([data_map, dist])

    return datalist


def update_data(datapool, environment, dbenv):
    '''Update data in the database given the datasource 'data'
    '''
    data = datapool[0]
    dist = datapool[1]
    print("Update data [%s] environment [%s]" %
          (data[0], environment))

    # TODO: Remove!
    if data[2] == None:
        print("ERROR: Not implemented data set hander")
        return

    dbmod = importlib.import_module("lib.db.%s" % dbenv)
    dbclient = dbmod.DBClient(
        "gouv_fr_covid19_emergency_room_visits", environment)

    dci = DataCollectionImporter(
        dbclient, "gouv_fr_covid19_emergency_room_visits")

    csv_content = requests.get(dist['contentUrl'])

    if not csv_content.ok:
        print("ERROR: getting the data file")

    with io.StringIO(csv_content.text) as fd:
        csv_file = csv.reader(fd, delimiter=',', quotechar='"')
        # Skip header
        next(csv_file)
        dci.import_data(csv_file, data[2])
    dci.remove_old_data()

    # For each table, insert the metadata
    dbclient.update_metadata("gouv_fr/metadata.json")
    dbclient.sync()
 
    print("Finished updating data [%s] environment [%s]"
          % (data[0], environment))


def import_data_gouv_fr(environment, ignore_errors, dbenv="google_firestore"):
    print("import_data_gouv_fr called [%s] [%s]" %
          (environment, ignore_errors))
    datalist = download_master_html()
    for data in datalist:
        update_data(data, environment, dbenv)
    print("import_data_gouv_fr finished")


if __name__ == '__main__':
    '''For (local) testing'''
    import_data_gouv_fr("prod", True, "python_json")
