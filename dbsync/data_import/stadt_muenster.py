'''
File which implements the data import of
the Stadt Muenster data set.
'''

# TODO: implement function, which updates data
# TODO: implement function, which imports one data set
# TODO: implement function, which opens the right repo
# TODO: implement function, which converts str to int

import hashlib
import csv
from data_import.lib.utils import import_data_collection, get_available_data_ids

def convert_2int(s):
    return int(s)

def convert_one_line(line):
    '''Converts one data line into json.
        Format of the imported data:
          0       1         2        3        4           5
        Gebiet, Datum, Bestaetigte Faelle, Gesundete, Todesfaelle

        I am not sure if I can use the german expression or /
        I have to translate them into english'''

    try:
        gesundete = None
        todesfaelle = None

        if line[3] != '':
            gesundete = convert_2int(gesundete)

        if line[4] != '':
            todesfaelle = convert_2int(todesfaelle)

        # always standard german time format DD/MM/YYYY
        row = {
            'gebiet': line[0],
            'datum': line[1],
            'bestaetigte faelle': line[2],
            'gesundete': gesundete,
            'todesfaelle': todesfaelle,
            'source': 'Stadt Muenster'
        }

        hash_str = line[0] + line[1] + line[2] + line[3] + line[4]
        return row, hashlib.sha256(hash_str.encode("utf-8")).hexdigest()

    except ValueError as value:
        print("ERROR converting [%s]: [%s]"(line, value))


def read_csv_file(tab_ref, data_available_ids, fname):
    with open(fname, newline='') as csvfile:
        content = csv.reader(csvfile, delimiter=',', quotechar='"')
        if content == None:
            print("No callback available for the data file [%s] - skipping" % fname)
            return
        import_data_collection(content, tab_ref, data_available_ids)

