#!/usr/bin/env python
#
# Update the COVID19 datapool postgres database
#
from lib.parse_args import parse_args_main_postgresql


DBSYNCDIR="/opt/covid19dp/wvv-covid19-datapool/covid19datapool_dbsync"


def get_available_import_modules():
    '''Return a list of the available import modules'''
    amodules = []
    for fname in os.listdir(DBSYNCDIR):
        if os.path.isdir(fname):
            upath = os.path.join(DBSYNCDIR, fname, "update.py")
            if os.path.isfile(upath):
                amodules.append(fname)
    return amodules


def main():
    dbenv, environment, ignore_errors = parse_args_main_postgresql()
    amodules = get_available_import_modules()
    for module in amodules:
        print("Handling module [%s] started" % module)
        import_module = importlib.import_module("%s.update" % module)
        import_module.update_dataset(environment, ignore_errors, dbenv)
        print("Handling module [%s] finished" % module)


if __name__ == '__main__':
    main()
