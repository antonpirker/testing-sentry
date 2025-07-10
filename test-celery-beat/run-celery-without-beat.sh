#!/usr/bin/env bash

# exit on first error
set -euo pipefail

# Install uv if it's not installed
if ! command -v uv &> /dev/null; then
    curl -LsSf https://astral.sh/uv/install.sh | sh
fi

# Delete Celery beat schedule because because when switching versions
# a wrong schedule will cause strange errors
rm -f celerybeat-schedule

# Delete redis database (empty the queue)
rm -rf dump.rdb

# Run redis
redis-server --daemonize yes

# Run Celery without beat
uv run celery -A tasks.app worker \
    --loglevel=DEBUG \
    --concurrency=1
    # --max-tasks-per-child=2
