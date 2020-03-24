'''
Methods to get complete data sets.
'''
from google.cloud import firestore


def v1_get_all_cases_source(source):
    '''Get the complete data set'''
    print("Called v1_get_all_cases_source; source [%s]" % source)

    # Check if the source really exists
    if source not in ['johns_hopkins_github', 'ecdc_xlsx',
                      'gouv_fr_hospital_numbers']:
        print("Invalid source [%s]" % source)
        return []
    
    db = firestore.Client()
    tab_ref = db.collection(u"cases")\
                .document("sources")\
                .collection(source)

    result = []
    for doc in tab_ref.stream():
        result.append(doc.to_dict())
    print("Finished v1_get_all_cases_source; result size [%d]" % len(result))
    return result
