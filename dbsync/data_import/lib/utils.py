'''
Utility / common function for data import
'''

import os


def import_data_collection(collection, handle_one_data_line_cb,
                           tab_ref, data_available_ids):
    '''Generic function which imports all data from the collection.

    Collection can be e.g. a CSV file object or an xlsx-file iterator.
    '''
    # For logging only
    line_cnt = 0
    for line in collection:
        try:
            line_cnt += 1
            if line_cnt % 100 == 0:
                print("Handled [%d] entries" % line_cnt)
            data, sha = handle_one_data_line_cb(line)
            # If there is no need to process any further
            # (e.g. errornous line), a None is returned.
            if data is None:
                continue
            # First check, if the id is already in the database
            # based on the cache of ids.
            if sha in data_available_ids:
                #print("INFO: Document [%s] already exists "
                #      "(ID cache check)" % sha)
                continue
            # Writing data is limited - check if the data is
            # already in the DB first.
            if tab_ref.document(sha).get().exists:
                # Document (entry) already exists
                #print("INFO: Document [%s] already exists (DB check)" % sha)
                continue
            print("Adding document [%s]" % sha)
            #print(" [%s]" % data)
            tab_ref.document(sha).set(data)

        except Exception as ex:
            print("ERROR: line cannot be handled [%s]: [%s]" % (ex, line))


def get_available_data_ids(tab_ref):
    '''Retrieve all available ids (keys) of the collection'''

    print("get_available_data_ids called")
    data_available_ids = []
    print("get_available_data_ids read stream")
    doc_cnt = 0
    for doc in tab_ref.stream():
        doc_cnt += 1
        if doc_cnt % 100 == 0:
            print("get_available_data_ids read document [%d]" % doc_cnt)
        data_available_ids.append(doc.id)
    print("Loaded [%d] ids of data already available"
          % len(data_available_ids))
    print("get_available_data_ids finished")
    return data_available_ids


def ls(directory):
    '''List all files in the given directory'''
    print("ls [%s] [%s]"
          % (directory, ' '.join(list(os.listdir(directory)))))
