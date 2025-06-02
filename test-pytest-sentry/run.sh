#!/usr/bin/env bash

# exit on first error
# set -euo pipefail

# Install uv if it's not installed
if ! command -v uv &> /dev/null; then
    curl -LsSf https://astral.sh/uv/install.sh | sh
fi

# Configure `pytest-rerunfailures` (-s is for stopping at breakpoints)
export PYTEST_ADDOPTS="--reruns=5 -s"

# Run the flaky test multiple times
for i in $(seq 1)
do
    echo "Run $i:"
    source .venv/bin/activate && pytest
done
