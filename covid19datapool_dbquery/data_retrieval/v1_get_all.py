'''
Methods to get complete data sets.
'''

import json
import psycopg2


def v1_get_all_cases_source(environment, source):
    '''Get the complete data set'''
    print("Called v1_get_all_cases_source; source [%s] "
          "environment [%s]" % (source, environment))

    # Check for validity of environment
    if environment not in ['prod', 'test']:
        print("Invalid environment [%s]" % environment)
        return '["Invalid environment"]', 422

    print("Retrieving password")
    with open("password_postgresql_covid19ro.txt") as pwd_fd:
        pwd = pwd_fd.read()[:-1]
    print("Password successfully read")

    print("Retrieving PostgreSQL IP address")
    with open("postgresql_ip_address.txt") as ipa_fd:
        ip_address = ipa_fd.read()[:-1]
    print("PostgreSQL IP address is [%s]" % ip_address)

    connection = psycopg2.connect(
        user="covid19ro", database="covid19dp",
        password=pwd, host=ip_address)

    print("Retrieving sources")
    sources = {}
    cur = connection.cursor()
    cur.execute("select source, jmetadata from metadata")
    records = cur.fetchall()
    for rec in records:
        sources[rec[0]] = rec[1]
    print("Sources [%s]" % sources.keys())

    # Check if the source really exists
    if source not in sources.keys():
        print("Invalid source [%s]" % source)
        return '["Invalid source"]', 422

    def data_generator():
        doc_cnt = 0
        is_first_doc = True
        yield b"["
        yield json.dumps(sources[source]).encode()
        yield b",["
        print("Execute select jdata")
        cur.execute("select jdata from cases where source = %s", (source, ))
        records = cur.fetchall()
        for doc in records:
            # print("DOC [%s]" % doc)
            if not is_first_doc:
                yield ","
            yield json.dumps(doc[0])
            doc_cnt += 1
            is_first_doc = False
        print("v1_get_all_cases_source environment [%s] source [%s] "
              "send [%d] docs" % (environment, source, doc_cnt))
        yield b"]]"

    print("v1_get_all_cases_source finished")
    return data_generator, 200
