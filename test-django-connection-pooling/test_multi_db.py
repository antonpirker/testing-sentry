#!/usr/bin/env python
"""Test script to understand multi-database scenarios and how Sentry would handle them"""

import os
import django
from django.conf import settings

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.db import connections
from hello.models import Greeting

def test_multi_db_simulation():
    """Test what information is available for multi-database scenarios"""

    print("=== Multi-Database Analysis ===")

    # 1. Test how QuerySet stores database info
    print("\n1. QuerySet Database Information:")
    qs_default = Greeting.objects.all()
    print(f"   Default QuerySet.db: {qs_default.db}")
    print(f"   Default QuerySet.db.alias: {getattr(qs_default.db, 'alias', 'NOT_FOUND')}")
    print(f"   Default QuerySet._db: {getattr(qs_default, '_db', 'NOT_FOUND')}")

    qs_using = Greeting.objects.using('default')
    print(f"   Using QuerySet.db: {qs_using.db}")
    print(f"   Using QuerySet.db.alias: {getattr(qs_using.db, 'alias', 'NOT_FOUND')}")
    print(f"   Using QuerySet._db: {getattr(qs_using, '_db', 'NOT_FOUND')}")

    # 2. Test database wrapper information
    print("\n2. Database Wrapper Information:")
    db = connections['default']
    print(f"   Database wrapper: {db}")
    print(f"   Database alias: {db.alias}")
    print(f"   Database vendor: {db.vendor}")
    print(f"   Database settings_dict: {db.settings_dict}")

    # 3. Test cursor information
    print("\n3. Cursor Information:")
    with connections['default'].cursor() as cursor:
        print(f"   Cursor: {cursor}")
        print(f"   Cursor.db: {getattr(cursor, 'db', 'NOT_FOUND')}")
        print(f"   Cursor.db.alias: {getattr(getattr(cursor, 'db', None), 'alias', 'NOT_FOUND')}")
        print(f"   Has connection: {hasattr(cursor, 'connection')}")
        if hasattr(cursor, 'connection'):
            print(f"   Connection info available: {hasattr(cursor.connection, 'info')}")

    # 4. Test get_connection_params() for various scenarios
    print("\n4. get_connection_params() Analysis:")
    for alias in connections:
        db = connections[alias]
        try:
            params = db.get_connection_params()
            print(f"   {alias}: {params}")
        except Exception as e:
            print(f"   {alias}: ERROR - {e}")

def simulate_sentry_data_collection():
    """Simulate how our improved Sentry data collection would work"""

    print("\n=== Sentry Data Collection Simulation ===")

    # Simulate our improved _set_db_data function
    def improved_set_db_data(cursor_or_db):
        # Get database wrapper
        db = cursor_or_db.db if hasattr(cursor_or_db, "db") else cursor_or_db

        print(f"\n--- Processing database: {db.alias} ---")

        # Method 1: Use cached config (our preferred approach)
        cached_config = {
            'default': {
                'db_name': settings.DATABASES['default']['NAME'],
                'host': settings.DATABASES['default']['HOST'],
                'port': settings.DATABASES['default']['PORT'],
                'vendor': db.vendor,
                'engine': settings.DATABASES['default']['ENGINE']
            }
        }

        config = cached_config.get(db.alias)
        if config:
            print(f"   ✅ Using cached config for {db.alias}")
            print(f"   DB_NAME: {config['db_name']}")
            print(f"   SERVER_ADDRESS: {config['host']}")
            print(f"   SERVER_PORT: {config['port']}")
            print(f"   DB_SYSTEM: {config['vendor']}")
            return True

        # Method 2: Use wrapper settings (fallback)
        try:
            connection_params = db.get_connection_params()
            print(f"   ✅ Using wrapper settings for {db.alias}")
            print(f"   DB_NAME: {connection_params.get('dbname', connection_params.get('database'))}")
            print(f"   SERVER_ADDRESS: {connection_params.get('host')}")
            print(f"   SERVER_PORT: {connection_params.get('port')}")
            print(f"   DB_SYSTEM: {db.vendor}")
            return True
        except Exception as e:
            print(f"   ❌ Wrapper settings failed: {e}")

        # Method 3: Skip rather than risk connection issues
        print(f"   ⚠️  Skipping database metadata collection for {db.alias}")
        return False

    # Test with cursor (simulating execute/executemany scenarios)
    print("\n1. Testing with cursor (execute scenario):")
    with connections['default'].cursor() as cursor:
        improved_set_db_data(cursor)

    # Test with database wrapper directly
    print("\n2. Testing with database wrapper:")
    improved_set_db_data(connections['default'])

if __name__ == '__main__':
    test_multi_db_simulation()
    simulate_sentry_data_collection()
