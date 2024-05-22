#!/usr/bin/env bash

# exit on first error
set -xe

# create and activate virtual environment
python -m venv .venv
source .venv/bin/activate

# Install (or update) requirements
python -m pip install -r requirements.txt

pkill redis-server || true
sleep 1
rm -rf dump.rdb
redis-server --daemonize yes

# Run program
python main.py