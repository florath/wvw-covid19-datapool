'''
Metadata stuff
'''

import datetime
import json


def update_metadata(database, mdpath, environment, project):
    '''Updates the metadata with the data at the given path for the
    given environment.
    '''
    print("update_metadata mdpath [%s] environment [%s] project [%s]"
          % (mdpath, environment, project))
    meta_ref = database.document(
        "covid19datapool/%s/%s/metadata" % (environment, project))
    with open(mdpath, "r") as filedesc:
        jdata = json.load(filedesc)
        jdata['last_updated'] = datetime.datetime.now().timestamp()
    meta_ref.set(jdata)


def get_metadata_from_db(db, environment, project):
    '''Retreive the metadata document from the DB'''
    
    meta_ref = db.document(
        "covid19datapool/%s/%s/metadata" % (environment, project))

    return meta_ref.get().to_dict()
