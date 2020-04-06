'''
Metadata stuff
'''

import datetime
import json



def get_metadata_from_db(db, environment, project):
    '''Retreive the metadata document from the DB'''
    
    meta_ref = db.document(
        "covid19datapool/%s/%s/metadata" % (environment, project))

    return meta_ref.get().to_dict()
