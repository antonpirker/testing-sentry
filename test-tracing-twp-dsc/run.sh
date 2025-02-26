#!/usr/bin/env bash

set -euo pipefail

python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

# see Procfile for the commands that are run
honcho start
