#!/usr/bin/env python

import datetime
import time
import json
from flask import Flask, request, Response
from data_retrieval.v1_get_all import v1_get_all_cases_source


app = Flask(__name__)


@app.route('/v1/get_all/<source>')
def lv1_get_all_cases_source(source):
    environment = request.args.get("env", default="prod", type=str)
    rgenerator, rcode = v1_get_all_cases_source(environment, source)
    response = app.response_class(
        status=rcode,
        response=rgenerator(),
        mimetype='application/json'
    )
    return response


@app.route("/time/")
def time_url():
    def streamer():
        for i in range(100):
            yield "<p>{}</p>".format(datetime.datetime.now())

    return Response(streamer())


@app.route('/')
def main():
    return 'Hello, World!'
