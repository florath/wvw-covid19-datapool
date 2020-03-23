#!/usr/bin/env python

from flask import Flask

from data_import.johns_hopkins_github import import_data_johns_hopkins_github
from data_import.ecdc_xlsx import import_data_ecdc_xlsx

app = Flask(__name__)

@app.route('/tasks/update_data/<source>')
def update_data(source):
    print("Update called", source)

    # ToDo: this should be a module and loaded during runtime
    if source == 'johns_hopkins_github':
        import_data_johns_hopkins_github()
    if source == 'ecdc_xlsx':
        import_data_ecdc_xlsx()
    else:
        print("*** ERROR: unknown source [%s]" % source)

    return "Update finished"

@app.route('/')
def main():
    return 'Hello, World!'

if __name__ == '__main__':
    main()
