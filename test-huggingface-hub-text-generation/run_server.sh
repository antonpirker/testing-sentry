#!/usr/bin/env bash

# exit on first error
set -euo pipefail

# Install uv if it's not installed
if ! command -v uv &> /dev/null; then
    curl -LsSf https://astral.sh/uv/install.sh | sh
fi

echo "Starting local text generation server accessible via huggingface_hub..."

# Run text generation server, accessible via huggingface_hub
uv run python local_server.py
