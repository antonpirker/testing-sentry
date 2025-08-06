# Django Connection Pooling Test Project

This project demonstrates Django 5.2.5 with PostgreSQL connection pooling using `psycopg[pool]==3.2.9` and tests for potential connection pool exhaustion issues with Sentry SDK integration.

## Overview

This test project was created to reproduce and investigate a user-reported issue where Django applications with connection pooling enabled experience "couldn't get a connection after X seconds" errors when using Sentry SDK.

## Features

- **Django 5.2.5** with latest connection pooling support
- **PostgreSQL 15** in Docker container
- **psycopg[pool]==3.2.9** for connection pooling
- **Sentry SDK** with Django integration
- **Test endpoints** to reproduce connection pool exhaustion
- **Admin interface** for database interaction testing

## Project Structure

```
test-django-connection-pooling/
├── README.md                   # This file
├── pyproject.toml              # Dependencies (Django 5.2.5 + psycopg[pool])
├── run.sh                      # Smart startup script
├── manage.py                   # Django management
├── mysite/                     # Main Django project
│   ├── settings.py            # PostgreSQL + connection pooling config
│   └── urls.py                # URL routing
└── hello/                      # Hello-world app with test endpoints
    ├── models.py              # Greeting model
    ├── views.py               # API endpoints + pool stress tests
    ├── admin.py               # Admin interface
    └── migrations/            # DB schema + sample data
```

## Quick Start

### 1. Start the Server

```bash
cd test-django-connection-pooling
./run.sh
```

The `run.sh` script will:
- Install `uv` if not available
- Start PostgreSQL Docker container (port 5434)
- Run Django migrations
- Start Django development server (port 8000)

### 2. Access the Application

- **Main API**: http://localhost:8000/
- **Django Admin**: http://localhost:8000/admin/ (admin/admin)
- **Error Test**: http://localhost:8000/error/

## Connection Pool Configuration

The project is configured with a **small connection pool** to easily reproduce exhaustion:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "OPTIONS": {
            "pool": {
                "min_size": 1,      # Minimum connections
                "max_size": 3,      # Maximum connections (small for testing)
                "timeout": 10,      # Connection timeout in seconds
            }
        },
    }
}
```

## Testing Connection Pool Exhaustion

### Available Test Endpoints

| Endpoint | Purpose | Expected Result |
|----------|---------|----------------|
| `/test/pool-stress/` | **Stress test with 15 concurrent threads** | Should show connection timeout errors |
| `/test/sentry-db-interaction/` | **Test Sentry SDK + database operations** | May fail with connection timeouts |
| `/test/connection-leak/` | **Test for connection leaks** | Shows connection acquisition attempts |

### 1. Pool Stress Test

This test creates 15 concurrent threads (more than the `max_size=3`) to exhaust the connection pool:

```bash
curl -s http://localhost:8000/test/pool-stress/ | jq '.errors'
```

**Expected output:**
```json
[
  "Thread 3: ERROR - couldn't get a connection after 10.00 sec",
  "Thread 4: ERROR - couldn't get a connection after 10.00 sec",
  ...
]
```

### 2. Sentry Database Interaction Test

Tests how Sentry SDK interacts with database operations:

```bash
curl -s http://localhost:8000/test/sentry-db-interaction/
```

**If Sentry is causing issues, you'll see:**
```json
{
  "error": "couldn't get a connection after 10.00 sec"
}
```

### 3. Connection Leak Simulation

Tests for potential connection leaks:

```bash
curl -s http://localhost:8000/test/connection-leak/ | jq '.errors | length'
```

### 4. Multiple Concurrent Requests

Test with multiple simultaneous requests:

```bash
# Run 5 concurrent requests to stress the pool
for i in {1..5}; do
  curl -s http://localhost:8000/ &
done
wait
```

## Reproducing the User-Reported Issue

The user reported: *"couldn't get a connection after X seconds"* with Django 5.2.4 + psycopg[pool]==3.2.9 + Sentry SDK.

### Steps to Reproduce:

1. **Start the server**: `./run.sh`
2. **Run stress test**: `curl http://localhost:8000/test/pool-stress/`
3. **Check for errors**: Look for "couldn't get a connection after 10.00 sec"

### Expected Results:

- ✅ **Connection timeouts occur** when concurrent requests > pool max_size
- ✅ **Sentry operations may fail** with connection exhaustion
- ✅ **Pool recovery** after connections are released

## Monitoring and Debugging

### View Current Pool Status

The main endpoint shows connection pool information:

```bash
curl -s http://localhost:8000/ | jq '.connection_info'
```

### Check PostgreSQL Connections

Connect to the PostgreSQL container to monitor active connections:

```bash
docker exec -it postgres-test psql -U postgres -d test_db
```

```sql
-- Show active connections
SELECT pid, usename, application_name, client_addr, state, query_start
FROM pg_stat_activity
WHERE datname = 'test_db';

-- Count connections by state
SELECT state, count(*)
FROM pg_stat_activity
WHERE datname = 'test_db'
GROUP BY state;
```

### Django Admin Testing

Use the admin interface to perform database operations:
1. Go to http://localhost:8000/admin/
2. Login with `admin` / `admin`
3. Add/edit/delete greetings while running stress tests

## Configuration Options

### Adjust Pool Size

Edit `mysite/settings.py` to modify pool behavior:

```python
"pool": {
    "min_size": 2,      # Increase for more persistent connections
    "max_size": 10,     # Increase to handle more concurrent requests
    "timeout": 30,      # Increase timeout for slower operations
}
```

### Disable Connection Pooling

To test without pooling, comment out the pool configuration:

```python
# "OPTIONS": {
#     "pool": {
#         "min_size": 1,
#         "max_size": 3,
#         "timeout": 10,
#     }
# },
```

### Disable Sentry SDK

To test if Sentry is causing the issue, comment out Sentry initialization in `settings.py`:

```python
# sentry_sdk.init(...)
```

## Common Issues and Solutions

### Issue: "couldn't get a connection after X seconds"

**Possible causes:**
1. **Too many concurrent requests** for the pool size
2. **Long-running database operations** holding connections
3. **Sentry SDK** not properly releasing connections
4. **Connection leaks** in application code

**Solutions:**
1. **Increase pool max_size** in settings
2. **Increase timeout** for slow operations
3. **Review Sentry configuration** for connection handling
4. **Use connection.close()** explicitly in problematic views

### Issue: Pool exhaustion during testing

This is **expected behavior** with the small pool size (`max_size=3`). The test is designed to trigger this condition.

## Environment Details

- **Python**: 3.12+
- **Django**: 5.2.5
- **PostgreSQL**: 15 (Docker)
- **psycopg**: 3.2.9 with pool extras
- **Sentry SDK**: Latest with Django integration

## Contributing

To test different scenarios:

1. Modify pool configuration in `settings.py`
2. Add new test endpoints in `hello/views.py`
3. Update URL patterns in `hello/urls.py`
4. Run tests with `curl` or Django admin interface

## Support

This project is specifically designed to reproduce and test connection pooling issues with Django + PostgreSQL + Sentry SDK. Use the provided test endpoints to isolate and debug connection pool exhaustion problems.
