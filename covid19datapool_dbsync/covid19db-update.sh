#!/bin/bash
#
# Updates the postgresql database

set -e
set -x

source /opt/covid19dp/venv/bin/activate
cd /opt/covid19dp/wvv-covid19-datapool/covid19datapool_dbsync
export PYTHONPATH=${PWD}
python /opt/covid19dp/wvv-covid19-datapool/covid19datapool_dbsync/covid19-update.py
