#!/usr/bin/env bash

# exit on first error
set -euo pipefail

reset

# Delete Celery beat schedule because because when switching versions
# a wrong schedule will cause strange errors
rm -f celerybeat-schedule

# create and activate virtual environment
python -m venv .venv
source .venv/bin/activate

# Install (or update) requirements
pip install -r requirements.txt

redis-server --daemonize yes

# Run Celery and beat in the same process
celery -A tasks.app worker \
    --beat \
    --loglevel=DEBUG \
    --concurrency=1
