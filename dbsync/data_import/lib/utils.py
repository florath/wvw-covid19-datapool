'''
Utility / common function for data import
'''

def import_data_collection(collection, handle_one_data_line_cb,
                           tab_ref, data_available_ids):
    '''Generic function which imports all data from the collection.

    Collection can be e.g. a CSV file object or an xlsx-file iterator.
    '''
    try:
        # Skip header
        next(collection)
        for line in collection:
            data, sha = handle_one_data_line_cb(line)
            # First check, if the id is already in the database
            # based on the cache of ids.
            if sha in data_available_ids:
                print("INFO: Document [%s] already exists "
                      "(ID cache check)" % sha)
                continue
            # Writing data is limited - check if the data is
            # already in the DB first.
            if tab_ref.document(sha).get().exists:
                # Document (entry) already exists
                print("INFO: Document [%s] already exists (DB check)" % sha)
                continue
            tab_ref.document(sha).set(data)

    except StopIteration as si:
        print("ERROR: StopIteration error in file [%s]" % fname)


def get_available_data_ids(tab_ref):
    '''Retrieve all available ids (keys) of the collection'''

    data_available_ids = []
    for doc in tab_ref.stream():
        data_available_ids.append(doc.id)
    print("Loaded [%d] ids of data already available"
          % len(data_available_ids))
    return data_available_ids
