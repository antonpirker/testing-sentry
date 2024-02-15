#!/usr/bin/env bash

# exit on first error
set -euo pipefail

reset

# create and activate virtual environment
python -m venv .venv
source .venv/bin/activate

# Install (or update) requirements
pip install -r requirements.txt

redis-server --daemonize yes

cd mysite

celery -A mysite.tasks.app worker \
    --loglevel=DEBUG \
    -B \
    -c 1 \
    --scheduler django_celery_beat.schedulers:DatabaseScheduler