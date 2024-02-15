#!/usr/bin/env bash

# exit on first error
set -euo pipefail

# create and activate virtual environment
python -m venv .venv
source .venv/bin/activate

# Start task
curl -i -X GET http://localhost:5000/
