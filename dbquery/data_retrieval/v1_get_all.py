'''
Methods to get complete data sets.
'''

import json
from google.cloud import firestore


def v1_get_all_cases_source(environment, source):
    '''Get the complete data set'''
    print("Called v1_get_all_cases_source; source [%s] "
          "environment [%s]" % (source, environment))

    # Check for validity of environment
    if environment not in ['prod', 'test']:
        print("Invalid environment [%s]" % environment)
        return '["Invalid environment"]', 422

    # Check if the source really exists
    if source not in ['johns_hopkins_github', 'ecdc_cases',
                      'gouv_fr_covid19_emergency_room_visits',
                      'rki_cases']:
        print("Invalid source [%s]" % source)
        return '["Invalid source"]', 422

    db = firestore.Client()

    meta_ref = db.document(
        "covid19datapool/%s/%s/metadata" % (environment, source))
    metadata = meta_ref.get().to_dict()

    def data_generator():
        doc_cnt = 0
        is_first_doc = True
        yield b"["
        yield json.dumps(metadata).encode()
        yield b",["
        tab_ref = db.collection(
            "covid19datapool/%s/%s/data/collection" % (environment, source))
        for doc in tab_ref.stream():
            if not is_first_doc:
                yield ","
            yield json.dumps(doc.to_dict()).encode()
            doc_cnt += 1
            is_first_doc = False
        print("v1_get_all_cases_source environment [%s] source [%s] "
              "send [%d] docs" % (environment, source, doc_cnt))
        yield b"]]"

    print("v1_get_all_cases_source finished")
    return data_generator, 200
