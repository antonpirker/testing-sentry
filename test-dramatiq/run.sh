#!/usr/bin/env bash

set -euo pipefail
reset

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install requirements into virtual environment
pip install -r requirements.txt

# Run script that sends task to dramatiq worker
python main.py
