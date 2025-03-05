#!/usr/bin/env bash

set -euo pipefail

reset

python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

python main.py