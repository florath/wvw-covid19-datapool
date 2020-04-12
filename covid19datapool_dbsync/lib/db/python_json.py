'''
Database backend using a simple python json implementation
'''

import os
import json


class DBClient:
    '''DBClient implementation for python json backend'''

    def __init__(self, name, environment,
                 dirname="/tmp/covid19datapool"):
        self.__name = name
        self.__environment = environment
        self.__dirname = dirname
        self.__filename = os.path.join(self.__dirname, name + ".json")
        if not os.path.exists(self.__dirname):
            os.mkdir(self.__dirname)
        self.__values = {}
        if os.path.exists(self.__filename):
            with open(self.__filename) as json_fd:
                self.__values = json.load(json_fd)
        else:
            self.__values = {}

    def get_available_data_ids(self):
        '''Return all the ids of the complete dataset'''
        return list(self.__values.keys())

    def exists(self, hashv):
        '''Check if the id (hashv) already exists in the DB'''
        return hashv in self.__values

    def insert(self, hashv, value):
        '''Insert the key / value pair into the DB'''
        self.__values[hashv] = value

    def remove(self, hashv):
        '''Remove the entry'''
        del self.__values[hashv]

    def update_metadata(self, mdpath):
        '''Update the metadata in the DB'''
        print("TODO!!!!", self, mdpath)

    def sync(self):
        '''Make data permanent'''
        with open(self.__filename, "w") as json_fd:
            json_fd.write(json.dumps(self.__values))
