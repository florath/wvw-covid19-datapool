#!/usr/bin/env python

from flask import Flask

from update_data.johns_hopkins_github import update_data_johns_hopkins_github

app = Flask(__name__)

@app.route('/tasks/update_data/<source>')
def update_data(source):
    print("Update called", source)

    if source == 'johns_hopkins_github':
        update_data_johns_hopkins_github()
    else:
        print("*** ERROR: unknown source [%s]" % source)
    
    return "Update finished"

@app.route('/')
def main():
    return 'Hello, World!'

if __name__ == '__main__':
    main()
