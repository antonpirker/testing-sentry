#!/usr/bin/env bash

# exit on first error
set -xe

# Install uv if it's not installed
if ! command -v uv &> /dev/null; then
    curl -LsSf https://astral.sh/uv/install.sh | sh
fi

# Run the script
uv run uvicorn main:app --port 5000 --reload
