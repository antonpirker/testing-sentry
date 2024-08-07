#!/usr/bin/env bash

set -euo pipefail
reset

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install requirements into virtual environment
pip install -r requirements.txt

# Start a fresh redis server
pkill redis-server || true
sleep 1
rm -rf dump.rdb
redis-server --daemonize yes

# Start dramatiq worker
dramatiq --processes 1 main
