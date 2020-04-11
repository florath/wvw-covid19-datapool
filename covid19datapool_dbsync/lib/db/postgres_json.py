'''
Database backend using postgres and jsonb
'''

import os
import psycopg2
import json
import sys


DATA_TABLE = "cases"
METADATA_TABLE = "metadata"


class DBClient:

    def __init__(self, name, environment):
        self.__name = name
        self.__environment = environment

        pwd = os.getenv("COVID19DP_PASSWORD")
        self.__connection = psycopg2.connect(
            user="covid19usr", database="covid19dp", password=pwd)
        cur = self.__connection.cursor()
        cur.execute("select * from information_schema.tables "
                    "where table_name=%s",
                    (DATA_TABLE,))
        if not bool(cur.rowcount):
            print("ERROR: required tabled does not exitst")
            sys.exit(1)
        cur.close()
        self.__connection.commit()
        self.__exists_cur = self.__connection.cursor()
        self.__cur = self.__connection.cursor()

    def get_available_data_ids(self):
        ids = set()
        cur = self.__connection.cursor()
        cur.execute("select id from %s where source = %s",
                    (DATA_TABLE, self.__name,))
        records = cur.fetchall()
        for id in records:
            ids.add(id[0])
        return ids

    def exists(self, hashv):
        self.__exists_cur.execute(
            "select id from %s where source = %s and id = %s",
            (DATA_TABLE, self.__name, hashv, ))
        # print("RC", self.__exists_cur.rowcount)
        return self.__exists_cur.rowcount > 0
        
    def insert(self, hashv, value):
        self.__cur.execute(
            "insert into %s(id, source, jdata) values (%s, %s, %s)",
            (DATA_TABLE, hashv, self.__name, json.dumps(value)))

    def remove(self, hashv):
        self.__cur.execute(
            "delete from %s where id = %s",
            (DATA_TABLE, hashv, ))

    def update_metadata(self, mdpath):
        print("TODO!!!!")

    def sync(self):
        '''Make data permanent'''
        self.__cur.close()
        self.__connection.commit()
        self.__cur = self.__connection.cursor()
