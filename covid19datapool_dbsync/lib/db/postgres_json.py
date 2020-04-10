'''
Database backend using postgres and jsonb
'''

import psycopg2
import json


PSQL_CREATE_TABLE = '''
CREATE TABLE covid19json (
  id CHAR(64) NOT NULL PRIMARY KEY,
  source TEXT NOT NULL,
  jdata JSONB NOT NULL
)'''


class DBClient:

    def __init__(self, name, environment):
        self.__name = name
        self.__environment = environment

        self.__connection = psycopg2.connect(
            user="florath", database="jsontst")
        cur = self.__connection.cursor()
        cur.execute("select * from information_schema.tables "
                    "where table_name=%s",
                    ('covid19json',))
        if not bool(cur.rowcount):
            print("Create table")
            cur.execute(PSQL_CREATE_TABLE)
        cur.close()
        self.__connection.commit()
        self.__exists_cur = self.__connection.cursor()
        self.__cur = self.__connection.cursor()

    def get_available_data_ids(self):
        ids = set()
        cur = self.__connection.cursor()
        cur.execute("select id from covid19json where source = %s", (self.__name,))
        records = cur.fetchall()
        for id in records:
            ids.add(id[0])
        return ids

    def exists(self, hashv):
        self.__exists_cur.execute(
            "select id from covid19json where source = %s and id = %s", (self.__name, hashv, ))
        # print("RC", self.__exists_cur.rowcount)
        return self.__exists_cur.rowcount > 0
        
    def insert(self, hashv, value):
        self.__cur.execute(
            "insert into covid19json(id, source, jdata) values (%s, %s, %s)",
            (hashv, self.__name, json.dumps(value)))

    def remove(self, hashv):
        self.__cur.execute(
            "delete from covid19json where id = %s",
            (hashv, ))

    def update_metadata(self, mdpath):
        print("TODO!!!!")

    def sync(self):
        '''Make data permanent'''
        self.__cur.close()
        self.__connection.commit()
        self.__cur = self.__connection.cursor()
