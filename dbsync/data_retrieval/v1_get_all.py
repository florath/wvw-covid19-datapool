'''
Methods to get complete data sets.
'''

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
    if source not in ['johns_hopkins_github', 'ecdc_xlsx',
                      'gouv_fr_covid19_emergency_room_visits']:
        print("Invalid source [%s]" % source)
        return '["Invalid source"]', 422
    
    db = firestore.Client()

    meta_ref = db.document(
        "covid19datapool/%s/%s/metadata" % (environment, source))
    metadata = meta_ref.get().to_dict()
    
    tab_ref = db.collection(
        "covid19datapool/%s/%s/data/collection" % (environment, source))

    result = []
    for doc in tab_ref.stream():
        result.append(doc.to_dict())
    print("Finished v1_get_all_cases_source; result size [%d]" % len(result))
    return [metadata, result], 200
