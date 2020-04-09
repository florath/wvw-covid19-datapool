#!/usr/bin/env python
'''
Main file for dbsync / dbimport
'''

import json
import os
import importlib
from flask import Flask, request
from google.cloud import tasks_v2


# This is the way it is documented
# pylint: disable=invalid-name
app = Flask(__name__)


PROJECT = os.environ['GOOGLE_CLOUD_PROJECT']
LOCATION = "europe-west3"
QUEUE = "data-import"


# This is an internally used interface
# which will change at any time.
# Don't use it!
@app.route('/v1/trigger/import_data/<source>')
def import_data_trigger(source):
    '''This triggers the import via a Cloud Task'''
    print("import_data_trigger called for [%s]" % source)

    environment = request.args.get("env", default="prod", type=str)
    ignore_errors = request.args.get("ignore-errors", default=True, type=bool)
    print("import_data_trigger environment [%s] ignore-errors [%s]"
          % (environment, ignore_errors))

    if environment not in ["prod", "test"]:
        print("Wrong paramter for environment [%s]" % environment)
        return "Wrong input parameter", 422

    # Data passed to the real funtion
    jdata = {
        'source': source,
        'environment': environment,
        'ignore-errors': ignore_errors
    }

    client = tasks_v2.CloudTasksClient()
    parent = client.queue_path(PROJECT, LOCATION, QUEUE)

    # Construct the request body.
    task = {
        'app_engine_http_request': {  # Specify the type of request.
            'http_method': 'POST',
            'relative_uri': '/v1/task/import_data',
            'body': json.dumps(jdata).encode()
        }
    }

    response = client.create_task(parent, task)

    print("Created task {}".format(response.name))
    print("import_data_trigger finished for [%s]" % source)
    return "import_data_trigger ok", 200


def get_available_import_modules():
    '''Return a list of the available import modules'''
    amodules = []
    for fname in os.listdir():
        if os.path.isdir(fname):
            upath = os.path.join(fname, "update.py")
            if os.path.isfile(upath):
                amodules.append(fname)
    return amodules


@app.route('/v1/task/import_data', methods=['POST', ])
def import_data():
    '''The real import function'''
    jdata = json.loads(request.get_data(as_text=True))
    print("import_data called with parameters [%s]" % jdata)

    source = jdata['source']

    amodules = get_available_import_modules()

    if source not in amodules:
        print("*** ERROR: unknown source [%s]" % source)
        return "Unknown source", 421

    import_module = importlib.import_module("%s.update" % source)
    import_module.update_dataset(
        jdata['environment'], jdata['ignore-errors'])

    print("import_data finished for [%s]" % source)
    return "import_data ok", 200


@app.route('/')
def main():
    '''Test function'''
    return 'Hello, World!'


def main_test():
    '''Test function called when main is called'''
    amodules = get_available_import_modules()
    for module in amodules:
        import_module = importlib.import_module("%s.update" % module)
        print(import_module.update_dataset)


if __name__ == '__main__':
    main_test()
