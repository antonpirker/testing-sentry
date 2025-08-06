#!/usr/bin/env bash

# exit on first error
set -euo pipefail

# Install uv if it's not installed
if ! command -v uv &> /dev/null; then
    curl -LsSf https://astral.sh/uv/install.sh | sh
fi

# Run the django project
uv run python manage.py migrate
uv run python manage.py runserver 0.0.0.0:8000
