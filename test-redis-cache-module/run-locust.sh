#!/usr/bin/env bash

# exit on first error
set -xe

# create and activate virtual environment
python -m venv .venv
source .venv/bin/activate

locust