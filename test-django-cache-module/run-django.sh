#!/usr/bin/env bash

# exit on first error
set -xe

# create and activate virtual environment
python -m venv .venv
source .venv/bin/activate

# Install (or update) requirements
python -m pip install -r requirements.txt

pkill redis-server || true
sleep 1
rm -rf dump.rdb
redis-server --daemonize yes

# run migrations
# cd mysite && ./manage.py migrate && cd ..

# Run Django application on localhost:8000 (DEBUG)
# cd mysite && ./manage.py runserver 0.0.0.0:8000 && cd ..

# Run Django application on localhost:8000 (PRODUCTION)
# cd mysite && mprof run --multiprocess --output "../mprofile_$(date +%Y%m%d%H%M%S).dat" gunicorn wsgi && cd ..
cd mysite && gunicorn --log-level 'debug' wsgi && cd ..
