'''
Data Importer

This file contains helper and utility functions
to update the tables
'''

import copy
import hashlib
import traceback
import sys


def get_available_data_ids(tab_ref):
    '''Retrieve all available ids (keys) of the collection'''

    print("get_available_data_ids called")
    data_available_ids = []
    print("get_available_data_ids read stream")
    doc_cnt = 0
    for doc in tab_ref.stream():
        doc_cnt += 1
        if doc_cnt % 500 == 0:
            print("get_available_data_ids read document [%d]" % doc_cnt)
        data_available_ids.append(doc.id)
    print("Loaded [%d] ids of data already available"
          % len(data_available_ids))
    print("get_available_data_ids finished")
    return data_available_ids


class DataCollectionImporter:

    def __init__(self, tab_ref, name):
        self.__tab_ref = tab_ref
        self.__name = name
        self.__data_available_ids = get_available_data_ids(tab_ref)
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
                data_sha_list = handle_one_data_line_cb(line)
                for ds in data_sha_list:
                    data = ds[0]
                    sha = hashlib.sha256(ds[1].encode("utf-8")).hexdigest()
                    # If there is no need to process any further
                    # (e.g. errornous line), a None is returned.
                    if data is None:
                        continue
                    # Remove the sha from the list
                    if sha in self.__to_be_deleted_ids:
                        self.__to_be_deleted_ids.remove(sha)
                    # First check, if the id is already in the database
                    # based on the cache of ids.
                    if sha in self.__data_available_ids:
                        # print("INFO: Document [%s] already exists "
                        #       "(ID cache check)" % sha)
                        continue
                    # Writing data is limited - check if the data is
                    # already in the DB first.
                    if self.__tab_ref.document(sha).get().exists:
                        # Document (entry) already exists
                        continue
                    print("[%s] Adding document [%s]" % (self.__name, sha))
                    self.__tab_ref.document(sha).set(data)

            except Exception as ex:
                print("ERROR: line cannot be handled [%s]: [%s]" % (ex, line))
                traceback.print_exc(file=sys.stdout)

    def remove_old_data(self):
        '''Remove possible old data'''
        print("[%s] remove_old_data called; count [%d]"
              % (self.__name, len(self.__to_be_deleted_ids)))
        for tbd in self.__to_be_deleted_ids:
            print("[%s] Deleting document [%s]" % (self.__name, tbd))
            self.__tab_ref.document(tbd).delete()
        print("[%s] remove_old_data finished" % self.__name)
