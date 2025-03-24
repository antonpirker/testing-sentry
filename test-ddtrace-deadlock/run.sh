#!/usr/bin/env bash

# exit on first error
# set -euo pipefail

# Install uv if it's not installed
if ! command -v uv &> /dev/null; then
    curl -LsSf https://astral.sh/uv/install.sh | sh
fi

uv run ddtrace-run --profiling flask run --host=0.0.0.0 --port=8000
