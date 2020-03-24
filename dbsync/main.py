#!/usr/bin/env python

import json
from flask import Flask

from data_import.johns_hopkins_github import import_data_johns_hopkins_github
from data_import.ecdc_xlsx import import_data_ecdc_xlsx
from data_import.gouv_fr import import_data_gouv_fr
from data_retrieval.v1_get_all import v1_get_all_cases_source


app = Flask(__name__)


@app.route('/v1/get_all/cases/source/<source>')
def lv1_get_all_cases_source(source):
    response = app.response_class(
        response=json.dumps(v1_get_all_cases_source(source)),
        status=200,
        mimetype='application/json'
    )
    return response


# This is an internally used interface
# which will change at any time.
# Don't use it!
@app.route('/tasks/update_data/<source>')
def update_data(source):
    print("Update called", source)

    # ToDo: this should be a module and loaded during runtime
    if source == 'johns_hopkins_github':
        import_data_johns_hopkins_github()
    if source == 'ecdc_xlsx':
        import_data_ecdc_xlsx()
    if source == 'gouv_fr':
        import_data_gouv_fr()
    else:
        print("*** ERROR: unknown source [%s]" % source)

    return "Update finished"


@app.route('/')
def main():
    return 'Hello, World!'


if __name__ == '__main__':
    main()
