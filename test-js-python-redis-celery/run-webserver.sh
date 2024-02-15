#!/usr/bin/env bash

# exit on first error
set -euo pipefail

reset

# create and activate virtual environment
python -m venv .venv
source .venv/bin/activate

python -m http.server 5000