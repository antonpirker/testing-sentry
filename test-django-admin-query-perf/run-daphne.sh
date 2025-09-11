#!/usr/bin/env bash

# exit on first error
set -euo pipefail

# Install uv if it's not installed
if ! command -v uv &> /dev/null; then
    curl -LsSf https://astral.sh/uv/install.sh | sh
fi

# Run Django with Daphne
uv run daphne -b 0.0.0.0 -p 8000 django_admin_sentry_perf.asgi:application
