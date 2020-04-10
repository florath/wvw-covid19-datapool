'''
Data Importer

This file contains helper and utility functions
to update the tables
'''

import copy
import hashlib
import traceback
import sys


class DataCollectionImporter:
    '''Imports a data collection

    This class can handle arbritrary inputs: they just need to
    be iterable.
    '''
    def __init__(self, dbclient, name):
        self.__dbclient = dbclient
        self.__name = name
        self.__data_available_ids = dbclient.get_available_data_ids()
        print("Available data rows [%d]" % len(self.__data_available_ids))
        self.__line_cnt = 0
        self.__add_cnt = 0
        self.__data_row_cnt = 0
        self.__exists_cnt = 0

    def import_data(self, collection, handle_one_data_line_cb):
        '''Generic function which imports all data from the collection.

        Collection can be e.g. a CSV file object or an xlsx-file iterator.
        '''
        # For logging only
        for line in collection:
            try:
                self.__line_cnt += 1
                if self.__line_cnt % 500 == 0:
                    print("[%s] Handled [%d] entries" %
                          (self.__name, self.__line_cnt))
                data_hashv_list = handle_one_data_line_cb(line)
                for dhv in data_hashv_list:
                    self.__data_row_cnt += 1
                    data = dhv[0]
                    hashv = hashlib.sha256(dhv[1].encode("utf-8")).hexdigest()
                    # If there is no need to process any further
                    # (e.g. errornous line), a None is returned.
                    if data is None:
                        continue
                    # First check, if the id is already in the database
                    # based on the cache of ids.
                    # Remove the hashv from the list
                    if hashv in self.__data_available_ids:
                        self.__data_available_ids.remove(hashv)
                        continue
                    # Writing data is limited - check if the data is
                    # already in the DB first.
                    if self.__dbclient.exists(hashv):
                        # Document (entry) already exists
                        print("Document [%s] already exists (double document in original dataset!)" % (hashv,))
                        self.__exists_cnt += 1
                        continue
                    self.__add_cnt += 1
                    if self.__add_cnt % 500 == 0:
                        print("[%s] Adding document [%s]" % (self.__name, hashv))
                    self.__dbclient.insert(hashv, data)

            # There are *many* possible problems - because on the invalid data
            # or the input source.
            # pylint: disable=broad-except
            except Exception as ex:
                print("ERROR: line cannot be handled [%s]: [%s]" % (ex, line))
                traceback.print_exc(file=sys.stdout)
        print("Checked documents in this run [%d]" % self.__line_cnt)
        print("Added documents in this run [%d]" % self.__add_cnt)
        print("Data row count in this run [%d]" % self.__data_row_cnt)
        print("Exists count in this run [%d]" % self.__exists_cnt)

    def remove_old_data(self):
        '''Remove possible old data'''
        print("[%s] remove_old_data called; delete count [%d]"
              % (self.__name, len(self.__data_available_ids)))
        print("[%s] remove_old_data called; lines [%d]  added [%d]  data rows [%d]  exists [%d]"
              % (self.__name, self.__line_cnt, self.__add_cnt, self.__data_row_cnt, self.__exists_cnt))
        del_cnt = 0
        for tbd in self.__data_available_ids:
            del_cnt += 1
            if del_cnt % 500 == 0:
                print("[%s] Deleting document [%s]" % (self.__name, tbd))
            self.__dbclient.remove(tbd)
        print("[%s] remove_old_data finished" % self.__name)
