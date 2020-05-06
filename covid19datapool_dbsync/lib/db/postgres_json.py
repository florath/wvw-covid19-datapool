'''
Database backend using postgres and jsonb
'''

import datetime
import os
import json
import sys

import psycopg2


class DBClient:
    '''DBClient implementation for postgres json backend'''

    def __init__(self, name, environment):
        self.__name = name
        self.__environment = environment

        pwd = os.getenv("COVID19DP_PASSWORD")
        self.__connection = psycopg2.connect(
            user="covid19usr", database="covid19dp", password=pwd)
        cur = self.__connection.cursor()
        cur.execute("select * from information_schema.tables "
                    "where table_name=%s",
                    ('cases',))
        if not bool(cur.rowcount):
            print("ERROR: required tabled does not exitst")
            sys.exit(1)
        cur.close()
        self.__connection.commit()
        self.__exists_cur = self.__connection.cursor()
        self.__cur = self.__connection.cursor()

    def get_available_data_ids(self):
        '''Return all the ids of the complete dataset'''
        ids = set()
        cur = self.__connection.cursor()
        cur.execute("select id from cases where source = %s",
                    (self.__name,))
        records = cur.fetchall()
        for rid in records:
            ids.add(rid[0])
        return ids

    def exists(self, hashv):
        '''Check if the id (hashv) already exists in the DB'''
        self.__exists_cur.execute(
            "select id from cases where source = %s and id = %s",
            (self.__name, hashv, ))
        # print("RC", self.__exists_cur.rowcount)
        return self.__exists_cur.rowcount > 0

    def insert(self, hashv, value):
        '''Insert the key / value pair into the DB'''
        self.__cur.execute(
            "insert into cases(id, source, jdata) values (%s, %s, %s)",
            (hashv, self.__name, json.dumps(value)))

    def remove(self, hashv):
        '''Remove data with id from DB'''
        self.__cur.execute(
            "delete from cases where id = %s",
            (hashv, ))

    def update_metadata(self, mdpath):
        '''Update the metadata in the DB'''
        with open(mdpath, "r") as filedesc:
            jdata = json.load(filedesc)
            jdata['last_updated'] = datetime.datetime.now().timestamp()
        jdata = json.dumps(jdata)
        mdcur = self.__connection.cursor()
        mdcur.execute("INSERT INTO metadata(source, jmetadata) values (%s, %s) "
                      "ON CONFLICT ON CONSTRAINT metadata_pkey "
                      "DO UPDATE SET jmetadata = %s",
                      (self.__name, jdata, jdata))
        mdcur.close()
        self.__connection.commit()

    def sync(self):
        '''Make data permanent'''
        self.__cur.close()
        self.__connection.commit()
        self.__cur = self.__connection.cursor()
