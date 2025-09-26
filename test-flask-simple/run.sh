#!/usr/bin/env bash

# exit on first error
set -xe

# Install uv if it's not installed
if ! command -v uv &> /dev/null; then
    curl -LsSf https://astral.sh/uv/install.sh | sh
fi

uv run flask --app main run  --port 8000
