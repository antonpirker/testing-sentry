#!/usr/bin/env bash

# exit on first error
set -xe

# create and activate virtual environment
python -m venv .venv
source .venv/bin/activate

# Install (or update) requirements
python -m pip install -r requirements.txt


# Run Flask application on localhost:5000
flask --app main run

# Run Flask application with multithreading (port 8000)
# gunicorn main:app -w 1 --threads 12