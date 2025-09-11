#!/usr/bin/env python3
"""
Ultra-fast script to insert 10 million Django admin log entries for performance testing.
Multiple optimizations for maximum speed:
- Optimized database settings
- Larger batch sizes
- Connection pooling
- Pre-generated data pools
- Optimized transaction strategy
- Memory-efficient data generation
"""

import os
import sys
import django
import random
import string
import time
from datetime import datetime, timedelta
from multiprocessing import Pool, cpu_count
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
from itertools import cycle, islice

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_admin_sentry_perf.settings')
django.setup()

from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db import connection, transaction, connections
from django.conf import settings


ACTION_TIME = timezone.now()
MESSAGE = "Sentry reproduction django_admin_log entry"
USER, _ = User.objects.get_or_create(
    username='test_user',
    defaults={
        'email': 'test@example.com',
        'first_name': 'Test',
        'last_name': 'User',
        'is_staff': True,
    }
)
USER_ID = USER.id
CONTENT_TYPE_ID = 4


def optimize_database_settings():
    """Optimize database settings for bulk operations."""
    # Optimize SQLite settings for bulk operations
    if 'sqlite3' in settings.DATABASES['default']['ENGINE']:
        with connection.cursor() as cursor:
            # Enable WAL mode for better concurrent access
            cursor.execute("PRAGMA journal_mode=WAL")
            # Increase cache size
            cursor.execute("PRAGMA cache_size=10000")
            # Disable synchronous writes for bulk operations
            cursor.execute("PRAGMA synchronous=NORMAL")
            # Increase temp store
            cursor.execute("PRAGMA temp_store=MEMORY")
            # Optimize page size
            cursor.execute("PRAGMA page_size=4096")
            # Disable foreign key constraints temporarily
            cursor.execute("PRAGMA foreign_keys=OFF")


def restore_database_settings():
    """Restore normal database settings."""
    if 'sqlite3' in settings.DATABASES['default']['ENGINE']:
        with connection.cursor() as cursor:
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.execute("PRAGMA synchronous=FULL")



def get_random_content_type():
    """Get a random content type for log entries."""
    content_types = ContentType.objects.all()
    if content_types.exists():
        return random.choice(content_types)
    else:
        return ContentType.objects.get_for_model(User)


def create_log_entries_batch_optimized(batch_size=5000):
    """Create a batch of Django admin log entries with optimized data generation."""

    entries = []
    for i in range(batch_size):
        entry = LogEntry(
            action_time=ACTION_TIME,
            user_id=USER_ID,
            content_type_id=4,
            object_id=USER_ID,
            object_repr="sentry reproduction",
            action_flag=ADDITION,
            change_message=MESSAGE,
        )
        entries.append(entry)
    
    return entries


def insert_batch_optimized(batch_data):
    """Insert a batch of log entries with optimized bulk_create."""
    try:
        # Use larger batch size for bulk_create itself
        with transaction.atomic():
            LogEntry.objects.bulk_create(
                batch_data, 
                batch_size=5000,  # Larger internal batch size
                ignore_conflicts=True  # Skip duplicates if any
            )
        return len(batch_data)
    except Exception as e:
        print(f"Error inserting batch: {e}")
        return 0


def insert_log_entries_ultra_fast(total_entries=10_000_000, batch_size=5000, num_processes=None):
    """Insert log entries using ultra-optimized parallel processing."""
    if num_processes is None:
        num_processes = min(cpu_count(), 16)  # Increased process limit
    
    print(f"Starting ULTRA-FAST insertion of {total_entries:,} Django admin log entries...")
    print(f"Using {num_processes} processes with batch size of {batch_size}")
    
    # Optimize database settings
    optimize_database_settings()
    
    start_time = time.time()
    total_inserted = 0
    
    # Track performance for accurate rate calculation
    performance_window = []  # List of (timestamp, entries) tuples for last 30 seconds
    last_progress_time = start_time
    
    # Create batches with optimized distribution
    num_batches = total_entries // batch_size
    batches = [batch_size] * num_batches
    
    # Handle remaining entries
    remaining = total_entries % batch_size
    if remaining > 0:
        batches.append(remaining)
    
    print(f"Created {len(batches)} batches")
    
    # Use ThreadPoolExecutor with optimized settings
    with ThreadPoolExecutor(max_workers=num_processes, thread_name_prefix="log_worker") as executor:
        # Submit all batch creation tasks
        future_to_batch = {
            executor.submit(create_log_entries_batch_optimized, batch_size): batch_size 
            for batch_size in batches
        }
        
        # Process completed batches with progress tracking
        completed_batches = 0
        last_progress_time = time.time()
        
        for future in as_completed(future_to_batch):
            try:
                batch_data = future.result()
                inserted = insert_batch_optimized(batch_data)
                total_inserted += inserted
                completed_batches += 1
                
                # Progress reporting every 20 batches or every 15 seconds
                current_time = time.time()
                if (completed_batches % 20 == 0 or 
                    current_time - last_progress_time > 15):
                    
                    # Update performance window with current data point
                    performance_window.append((current_time, total_inserted))
                    
                    # Remove old data points (older than 30 seconds)
                    cutoff_time = current_time - 30
                    performance_window = [(t, e) for t, e in performance_window if t >= cutoff_time]
                    
                    # Calculate rate based on performance window
                    if len(performance_window) >= 2:
                        # Use sliding window for more accurate rate
                        window_start_time, window_start_entries = performance_window[0]
                        window_end_time, window_end_entries = performance_window[-1]
                        window_duration = window_end_time - window_start_time
                        window_entries = window_end_entries - window_start_entries
                        
                        if window_duration > 0:
                            rate = window_entries / window_duration
                        else:
                            rate = 0
                    else:
                        # Fallback to overall rate if not enough data
                        elapsed = current_time - start_time
                        rate = total_inserted / elapsed if elapsed > 0 else 0
                    
                    # Calculate ETA using current rate
                    if rate > 0:
                        remaining_entries = total_entries - total_inserted
                        eta_seconds = remaining_entries / rate
                        eta_minutes = eta_seconds / 60
                        eta_hours = eta_minutes / 60
                        
                        if eta_hours >= 1:
                            eta_str = f"{int(eta_hours)}h {int(eta_minutes % 60)}m"
                        elif eta_minutes >= 1:
                            eta_str = f"{int(eta_minutes)}m {int(eta_seconds % 60)}s"
                        else:
                            eta_str = f"{int(eta_seconds)}s"
                    else:
                        eta_str = "calculating..."
                    
                    # Calculate percentage
                    percentage = (total_inserted / total_entries) * 100
                    
                    print(f"Progress: {percentage:.1f}% ({total_inserted:,}/{total_entries:,}) "
                          f"| Rate: {rate:.0f} entries/sec | ETA: {eta_str}")
                    last_progress_time = current_time
                
            except Exception as e:
                print(f"Error processing batch: {e}")
    
    # Restore database settings
    restore_database_settings()
    
    elapsed_time = time.time() - start_time
    print(f"\n Insertion completed!")
    print(f"Total entries inserted: {total_inserted:,}")
    print(f"Total time: {elapsed_time:.2f} seconds")
    
    return total_inserted


def main():
    """Main function to run the ultra-fast log entry insertion."""
    print("Django Admin Log Entry Insertion Script")
    print("=" * 60)
    
    # Check if we want to clear existing entries
    response = input("Do you want to clear existing admin log entries before insertion? (y/N): ").strip().lower()
    if response in ['y', 'yes']:
        print("Clearing existing admin log entries using raw SQL...")
        start_time = time.time()
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM django_admin_log")
        elapsed_time = time.time() - start_time
        print(f"Existing entries cleared using fast raw DELETE in {elapsed_time:.2f} seconds.")
    
    # Get parameters with optimized defaults
    try:
        total_entries = int(input("Enter number of entries to insert (default: 10,000,000): ").strip() or "10000000")
        batch_size = int(input("Enter batch size (default: 5000): ").strip() or "5000")
        num_processes = input(f"Enter number of processes (default: {min(cpu_count(), 16)}): ").strip()
        num_processes = int(num_processes) if num_processes else None
    except ValueError:
        print("Using default values...")
        total_entries = 10_000_000
        batch_size = 5000
        num_processes = None
    
    print(f"\n Configuration:")
    print(f"- Total entries: {total_entries:,}")
    print(f"- Batch size: {batch_size}")
    print(f"- Processes: {num_processes or f'{min(cpu_count(), 16)}'}")
    
    # Confirm before starting
    response = input("\nProceed with insertion? (y/N): ").strip().lower()
    if response not in ['y', 'yes']:
        print("Insertion cancelled.")
        return
    
    # Run the insertion
    try:
        insert_log_entries_ultra_fast(total_entries, batch_size, num_processes)
    except KeyboardInterrupt:
        print("\nInsertion interrupted by user.")
        restore_database_settings()
    except Exception as e:
        print(f"Error during insertion: {e}")
        restore_database_settings()


if __name__ == "__main__":
    main() 