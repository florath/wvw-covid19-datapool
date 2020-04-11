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


def parse_args_main_postgresql():
    '''Parse command line arguments for postgresql main'''
    parser = argparse.ArgumentParser(description='common args')
    parser.add_argument('--dbenv', type=str, default="postgres_json",
                        help='Name of the database backend; '
                        'options: google_firestore, python_json, postgres_json')
    parser.add_argument('--environment', type=str, default="prod",
                        help='Name of the environment; '
                        'options: prod, test')
    parser.add_argument('--ignore_errors', type=bool, default=True,
                        help='Ignore possible non-fatal errors')
    args = parser.parse_args()
    return args.dbenv, args.environment, args.ignore_errors
