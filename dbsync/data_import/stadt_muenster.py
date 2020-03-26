'''
File which implements the data import of
the Stadt Muenster data set.
'''

# TODO: implement function, which reads a csv file
# TODO: implement function, which updates data
# TODO: implement function, which imports one data set
# TODO: implement function, which opens the right repo
# TODO: implement function, which converts str to int

import hashlib

def convert_one_line(line):
    '''Converts one data line into json.
        Format of the imported data:
          0       1         2        3        4           5
        Gebiet, Datum, Bestaetigte Faelle, Gesundete, Todesfaelle

        I am not sure if I can use the german expression or /
        I have to translate them into english'''

    try:
        # always standard german time format DD/MM/YYYY
        row = {
            'gebiet': line[0],
            'datum': line[1],
            'bestaetigte faelle': line[2],
            'gesundete': line[3],
            'todesfaelle': line[4]
            'source': 'Stadt Muenster'
        }

        hash_str = line[0] + line[1] + line[2] + line[3] + line[4]
        return row, hashlib.sha256(hash_str.encode("utf-8")).hexdigest()

    except ValueError as value:
        print("ERROR converting [%s]: [%s]"(line, value))

