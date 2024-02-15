#!/usr/bin/env bash

# exit on first error
set -euo pipefail

# create and activate virtual environment
python -m venv .venv
source .venv/bin/activate

# Start task
python -c 'import tasks; tasks.my_task.delay()'