#!/usr/bin/env bash

# exit on first error
set -euo pipefail

# Install uv if it's not installed
if ! command -v uv &> /dev/null; then
    curl -LsSf https://astral.sh/uv/install.sh | sh
fi

# Start Postgres server if not already running
if ! docker ps --format "table {{.Names}}" | grep -q "^postgres-test$"; then
    echo "Starting PostgreSQL container..."
    # Try to start existing container first
    if docker ps -a --format "table {{.Names}}" | grep -q "^postgres-test$"; then
        docker start postgres-test
    else
        # Create new container if it doesn't exist
        docker run --name postgres-test -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=test_db -p 5434:5432 -d postgres:15
    fi
else
    echo "PostgreSQL container is already running"
fi

# Run the django project
uv run python manage.py migrate
uv run python manage.py runserver 0.0.0.0:8000
