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
                      'gouv_fr_hospital_numbers']:
        print("Invalid source [%s]" % source)
        return '["Invalid source"]', 422
    
    db = firestore.Client()
    tab_ref = db.collection("covid19datapool")\
                .document(environment)\
                .collection("cases")\
                .document("sources")\
                .collection(source)

    result = []
    for doc in tab_ref.stream():
        result.append(doc.to_dict())
    print("Finished v1_get_all_cases_source; result size [%d]" % len(result))
    return result, 200
