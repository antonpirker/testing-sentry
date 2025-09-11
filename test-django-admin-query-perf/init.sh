#!/usr/bin/env bash

# exit on first error
set -euo pipefail

# Install uv if it's not installed
if ! command -v uv &> /dev/null; then
    curl -LsSf https://astral.sh/uv/install.sh | sh
fi

# Start PostgreSQL database in Docker
echo "Starting PostgreSQL database in Docker..."
docker run -d \
  --name postgres-demo \
  -e POSTGRES_DB=demo \
  -e POSTGRES_USER=admin \
  -e POSTGRES_PASSWORD=admin \
  -p 5439:5432 \
  postgres:15

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL to be ready..."
sleep 10

# Create database tables
uv run ./manage.py migrate

# Collect static files
uv run ./manage.py collectstatic --noinput

# Create superuser account
export DJANGO_SUPERUSER_USERNAME=admin
export DJANGO_SUPERUSER_EMAIL=admin@example.com
export DJANGO_SUPERUSER_PASSWORD=admin

uv run ./manage.py createsuperuser --noinput
echo "Username: admin"
echo "Password: admin"

# Create 10_000_000 rows in the database
echo "Creating 10_000_000 rows in the database..."
uv run python ./create_log_entries.py
