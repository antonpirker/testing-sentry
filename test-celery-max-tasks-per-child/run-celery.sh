#!/usr/bin/env bash

# exit on first error
set -euo pipefail

reset

# create and activate virtual environment
python -m venv .venv
source .venv/bin/activate

# Install (or update) requirements
pip install -r requirements.txt

reset 

redis-server --daemonize yes

export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES

celery -A tasks.app worker \
    --loglevel=DEBUG \
    -B \
    -c 1 \
    --max-tasks-per-child 10000 # > output.txt 2> error.txt
