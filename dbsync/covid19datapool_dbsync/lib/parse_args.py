'''
Parse command line arguments
'''

import argparse


def parse_args_common():
    '''Parse common command line arguments'''
    parser = argparse.ArgumentParser(description='common args.')
    parser.add_argument('--dbenv', type=str, required=True,
                        help='Name of the database backend; '
                        'options: google_firestore, python_json')
    args = parser.parse_args()
    return args.dbenv
