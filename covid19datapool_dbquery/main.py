#!/usr/bin/env python
'''
Main entry point for the REST interface
'''

from flask import Flask, request
from data_retrieval.v1_get_all import v1_get_all_cases_source


# This is the way it is documented
# pylint: disable=invalid-name
app = Flask(__name__)


@app.route('/v1/get_all/<source>')
def lv1_get_all_cases_source(source):
    '''Retrieve all cases entry point'''
    environment = request.args.get("env", default="prod", type=str)
    rgenerator, rcode = v1_get_all_cases_source(environment, source)
    response = app.response_class(
        status=rcode,
        response=rgenerator(),
        mimetype='application/json'
    )
    return response


@app.route('/')
def main():
    '''Test function - see if anything is set up correctly'''
    return 'Hello, World!'
