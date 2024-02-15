#!/usr/bin/env bash

# exit on first error
set -xe

# create and activate virtual environment
python -m venv .venv
source .venv/bin/activate

# Install (or update) requirements
python -m pip install -r requirements.txt

cd mysite

# run migrations
# ./manage.py migrate

# Run Django application on localhost:8000
daphne mysite.asgi:application
# ./manage.py runserver 0.0.0.0:8000
#gunicorn movie_search.project.asgi:application -k uvicorn.workers.UvicornWorker