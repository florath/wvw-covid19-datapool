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

    def __init__(self, dbclient, name):
        self.__dbclient = dbclient
        self.__name = name
        self.__data_available_ids = dbclient. get_available_data_ids()
        # List of all ids which are in the DB but not in the (current)
        # dataset (any longer).  These need to be deleted.
        self.__to_be_deleted_ids = copy.deepcopy(self.__data_available_ids)

    def import_data(self, collection, handle_one_data_line_cb):
        '''Generic function which imports all data from the collection.

        Collection can be e.g. a CSV file object or an xlsx-file iterator.
        '''
        # For logging only
        line_cnt = 0
        for line in collection:
            try:
                line_cnt += 1
                if line_cnt % 500 == 0:
                    print("[%s] Handled [%d] entries" %
                          (self.__name, line_cnt))
                data_hashv_list = handle_one_data_line_cb(line)
                for ds in data_hashv_list:
                    data = ds[0]
                    hashv = hashlib.sha256(ds[1].encode("utf-8")).hexdigest()
                    # If there is no need to process any further
                    # (e.g. errornous line), a None is returned.
                    if data is None:
                        continue
                    # Remove the hashv from the list
                    if hashv in self.__to_be_deleted_ids:
                        self.__to_be_deleted_ids.remove(hashv)
                    # First check, if the id is already in the database
                    # based on the cache of ids.
                    if hashv in self.__data_available_ids:
                        # print("INFO: Document [%s] already exists "
                        #       "(ID cache check)" % hashv)
                        continue
                    # Writing data is limited - check if the data is
                    # already in the DB first.
                    if self.__dbclient.exists(hashv):
                        # Document (entry) already exists
                        continue
                    print("[%s] Adding document [%s]" % (self.__name, hashv))
                    self.__dbclient.insert(hashv, data)

            except Exception as ex:
                print("ERROR: line cannot be handled [%s]: [%s]" % (ex, line))
                traceback.print_exc(file=sys.stdout)

    def remove_old_data(self):
        '''Remove possible old data'''
        print("[%s] remove_old_data called; count [%d]"
              % (self.__name, len(self.__to_be_deleted_ids)))
        for tbd in self.__to_be_deleted_ids:
            print("[%s] Deleting document [%s]" % (self.__name, tbd))
            self.__dbclient.remove(tbd)
        print("[%s] remove_old_data finished" % self.__name)
