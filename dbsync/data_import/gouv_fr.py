'''
Import the files from the French gouvernement
'''

import csv
import io
import requests
import json
import hashlib
from html.parser import HTMLParser
from data_import.lib.utils import import_data_collection, get_available_data_ids
from google.cloud import firestore
import dateutil.parser


URL_HTML_PAGE = "https://www.data.gouv.fr/en/datasets/donnees-relatives-a-lepidemie-du-covid-19"
DATA_DOWNLOAD_PREFIX = [
    'donnees-hospitalieres-covid19'
]


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


def handle_one_line(line):
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


def download_html():
    '''Download the main html page

    This is needed as this seams to be the only source of 
    the filenames.
    '''
    html_file = requests.get(URL_HTML_PAGE)
    parser = GouvFrHTMLParser()
    parser.feed(html_file.text)
    jdata = json.loads(parser.get_script_data())

    datadict = {}
    for dist in jdata['distribution']:
        if dist['@type'] != 'DataDownload':
            print("WARNING: distribution entry which is not a download [%s]"
                  % dist)
            continue
        for ddn in DATA_DOWNLOAD_PREFIX:
            if dist['name'].startswith(ddn):
                datadict[ddn] = dist
    # ToDo: Have an indicator when something new is added to the WEB page
    return datadict


def update_data(datadict):
    db = firestore.Client()
    tab_ref = db.collection(u"cases")\
                .document("sources")\
                .collection("gouv_fr_hospital_numbers")

    data_available_ids = get_available_data_ids(tab_ref)

    for key, val in datadict.items():
        csv_content = requests.get(val['contentUrl'])
        with io.StringIO(csv_content.text) as fd:
            csv_file = csv.reader(fd, delimiter=';', quotechar='"')
            # Skip header
            next(csv_file)
            import_data_collection(csv_file, handle_one_line, tab_ref, data_available_ids)


def import_data_gouv_fr():
    print("Called import_data_gouv_fr")
    datadict = download_html()
    update_data(datadict)
    print("Finished import_data_gouv_fr")


if __name__ == '__main__':
    '''For (local) testing'''
    import_data_gouv_fr()
