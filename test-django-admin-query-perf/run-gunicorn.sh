#!/usr/bin/env bash

# exit on first error
set -euo pipefail

# Install uv if it's not installed
if ! command -v uv &> /dev/null; then
    curl -LsSf https://astral.sh/uv/install.sh | sh
fi

uv sync

# Run Django with Gunicorn
export SENTRY_ENV=gunicorn
uv run gunicorn --bind 0.0.0.0:8000 --timeout 50000 django_admin_sentry_perf.wsgi:application

# Run Django with Gunicorn with async worker
# export SENTRY_ENV=gunicorn
# uv run gunicorn -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 django_admin_sentry_perf.asgi:application

# Run Django with uWSGI
# export SENTRY_ENV=uwsgi
# uv run uwsgi --http :8000 --module django_admin_sentry_perf.wsgi
