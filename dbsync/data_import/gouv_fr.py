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
from data_import.lib.utils import import_data_collection, get_available_data_ids
from google.cloud import firestore
import dateutil.parser


URL_HTML_PAGE = "https://www.data.gouv.fr/en/datasets/donnees-relatives-a-lepidemie-du-covid-19"


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


def handle_gouv_fr_hospital(line):
    '''Converts one line into json

    Format of the input data:

    0   1       2       3       4       5       6
    dep	sexe	jour	hosp	rea	rad	dc

    Where is:
    dep - department
    sexe - gender (0-total  1-???  2-???)
    jour - day
    hosp - Number of people currently hospitalized
    rea - Number of people currently in resuscitation or critical care
    rad - Total amount of patient that returned home
    dc - Total amout of deaths
    '''

    # ToDo: It's an assumption that 1 mean male and 2 female.
    #       The question was already asked on the web page.
    #       Waiting for an answer.

    # If sexe is == 0, then this is just the sum from
    # 1 (assumed man) and 2 (woman).
    # Therefore this can be skipped.
    if int(line[1]) == 0:
        return None, None

    ts = dateutil.parser.parse(line[2]).timestamp()

    nd = {
        'timestamp': ts,
        # Department is a string, e.g. 2A, 2B for Corsica
        'adm': ['FR', str(line[0])],
        'sex': 'm' if int(line[1]) == 1 else 'f',
        'hospitalized_current': int(line[3]),
        'critical_care_current': int(line[4]),
        'released_from_hospital_total': int(line[5]),
        'deaths_total': int(line[6])
    }
    sha_str = ''.join(line)
    return nd, hashlib.sha256(sha_str.encode("utf-8")).hexdigest()


def handle_gouv_fr_hospital_establishments(line):
    '''Converts one line into json'''
    print(line)
    assert False


def not_implemented():
    assert False


# These are the data which are needed for handling the different
# files.
# For each data set there is given:
# 0: the name of the dataset as it is used in the DB
# 1: a regular expression which matches the data file name
# 2: the callback which handles the data
DATA_MAPPING = [
    [ 'gouv_fr_hospital',
      re.compile('donnees-hospitalieres-covid19.*'),
      handle_gouv_fr_hospital ],
    [ 'gouv_fr_hospital_establishments',
      re.compile('donnees-hospitalieres-etablissements-covid19.*'),
      handle_gouv_fr_hospital_establishments],
    [ 'gouv_fr_covid19_daily',
      re.compile('sursaud-covid19-quotidien.*'),
      not_implemented],
    [ 'gouv_fr_covid19_weekly',
      re.compile('sursaud-covid19-hebdomadaire.*'),
      not_implemented],
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
      re.compile('metadonnee-urgenceshos-sosmedecins-covid19-quot.csv'),
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


def update_data(datapool):
    '''Update data in the database given the datasource 'data'
    '''
    data = datapool[0]
    dist = datapool[1]
    print("Update data [%s]" % data[0])

    print(data)
    
    db = firestore.Client()
    tab_ref = db.collection(u"cases")\
                .document("sources")\
                .collection(data[0])

    data_available_ids = get_available_data_ids(tab_ref)

    csv_content = requests.get(dist['contentUrl'])
    with io.StringIO(csv_content.text) as fd:
        csv_file = csv.reader(fd, delimiter=';', quotechar='"')
        # Skip header
        next(csv_file)
        import_data_collection(csv_file, data[2],
                               tab_ref, data_available_ids)
    print("Finished updating data [%s]" % data[0])


def import_data_gouv_fr():
    print("Called import_data_gouv_fr")
    datalist = download_master_html()
    print(datalist)
    for data in datalist:
        update_data(data)
    print("Finished import_data_gouv_fr")


if __name__ == '__main__':
    '''For (local) testing'''
    import_data_gouv_fr()
