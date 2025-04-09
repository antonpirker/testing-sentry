#!/usr/bin/env bash

# exit on first error
set -euo pipefail

# Install uv if it's not installed
if ! command -v uv &> /dev/null; then
    curl -LsSf https://astral.sh/uv/install.sh | sh
fi

# Set environment variables for OpenTelemetry
export USE_OTLP=true
export OTLP_ENDPOINT="http://localhost:5317"

# Run the producer
uv run python producer.py
