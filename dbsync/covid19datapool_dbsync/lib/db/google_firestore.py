'''
Database backend for Google Firestore
'''

import json
import datetime
from google.cloud import firestore


class DBClient:

    def __init__(self, name, environment):
        self.__name = name
        self.__environment = environment
        self.__db = firestore.Client()
        self.__tab_ref = self.__db.collection(
            "covid19datapool/%s/%s/data/collection"
            % (self.__environment, self.__name))

    def get_available_data_ids(self):
        '''Retrieve all available ids (keys) of the collection'''

        print("get_available_data_ids called")
        data_available_ids = []
        print("get_available_data_ids read stream")
        doc_cnt = 0
        for doc in self.__tab_ref.stream():
            doc_cnt += 1
            if doc_cnt % 500 == 0:
                print("get_available_data_ids read document [%d]" % doc_cnt)
            data_available_ids.append(doc.id)
        print("Loaded [%d] ids of data already available"
              % len(data_available_ids))
        print("get_available_data_ids finished")
        return data_available_ids

    def exists(self, hashv):
        '''Check if the hashv is really in the DB'''
        return self.__tab_ref.document(hashv).get().exists

    def insert(self, hashv, value):
        '''Set the value'''
        self.__tab_ref.document(hashv).set(value)

    def remove(self, hashv):
        '''Remove the entry'''
        self.__tab_ref.document(hashv).delete()

    def update_metadata(self, mdpath):
        '''Updates the metadata with the data at the given path for the
        given environment.
        '''
        print("update_metadata mdpath [%s]" % (mdpath,))
        meta_ref = self.__db.document(
            "covid19datapool/%s/%s/metadata" % (self.__environment, self.__name))
        with open(mdpath, "r") as filedesc:
            jdata = json.load(filedesc)
            jdata['last_updated'] = datetime.datetime.now().timestamp()
        meta_ref.set(jdata)

    def sync(self):
        '''Make data permanent'''
        pass
