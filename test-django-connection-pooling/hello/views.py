from django.shortcuts import render
from django.http import JsonResponse
from django.db import connection
from .models import Greeting
import sentry_sdk


def home(request):
    """Root route that queries greetings from database to demonstrate connection pooling"""
    try:
        # Get all greetings from database
        greetings = Greeting.objects.all()

        # Get connection info to show pool is being used
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            db_version = cursor.fetchone()[0]

        # Prepare response data
        greeting_data = [
            {
                "id": greeting.id,
                "message": greeting.message,
                "count": greeting.count,
                "created_at": greeting.created_at.isoformat(),
            }
            for greeting in greetings
        ]

        response_data = {
            "message": "Hello from Django with PostgreSQL Connection Pooling!",
            "database_version": db_version,
            "total_greetings": len(greeting_data),
            "greetings": greeting_data,
            "connection_info": {
                "backend": connection.vendor,
                "database": connection.settings_dict.get('NAME'),
                "host": connection.settings_dict.get('HOST'),
                "port": connection.settings_dict.get('PORT'),
                "connection_pooling": "enabled" if connection.settings_dict.get('OPTIONS', {}).get('pool') else "disabled"
            }
        }

        return JsonResponse(response_data, json_dumps_params={'indent': 2})

    except Exception as e:
        # Capture exception in Sentry
        sentry_sdk.capture_exception(e)
        return JsonResponse({
            "error": "Database connection failed",
            "message": str(e)
        }, status=500)


def error_test(request):
    """Test route to trigger an error for Sentry testing"""
    raise ValueError("This is a test error to demonstrate Sentry integration!")


def greeting_count_increment(request, greeting_id):
    """Increment the count of a specific greeting"""
    try:
        greeting = Greeting.objects.get(id=greeting_id)
        greeting.count += 1
        greeting.save()

        return JsonResponse({
            "message": f"Incremented count for greeting: {greeting.message}",
            "new_count": greeting.count
        })

    except Greeting.DoesNotExist:
        return JsonResponse({
            "error": "Greeting not found"
        }, status=404)
    except Exception as e:
        sentry_sdk.capture_exception(e)
        return JsonResponse({
            "error": "Failed to increment count",
            "message": str(e)
        }, status=500)


def connection_pool_stress_test(request):
    """Stress test to reproduce connection pool exhaustion issues"""
    import threading
    import time
    from django.db import connection, connections

    def long_running_query():
        """Simulate a long-running database operation"""
        try:
            with connection.cursor() as cursor:
                # Simulate a slow query that holds the connection
                cursor.execute("SELECT pg_sleep(5);")  # 5 second sleep
                cursor.execute("SELECT COUNT(*) FROM hello_greeting;")
                result = cursor.fetchone()
                return result[0]
        except Exception as e:
            return f"Error: {str(e)}"

    def create_multiple_connections():
        """Create multiple concurrent database connections"""
        threads = []
        results = []

        # Create more threads than our pool max_size (10)
        for i in range(15):
            def worker(thread_id):
                try:
                    # Each thread gets its own connection from the pool
                    greeting_count = Greeting.objects.count()
                    time.sleep(2)  # Hold the connection for 2 seconds
                    results.append(f"Thread {thread_id}: {greeting_count} greetings")
                except Exception as e:
                    results.append(f"Thread {thread_id}: ERROR - {str(e)}")

            thread = threading.Thread(target=worker, args=(i,))
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        return results

    try:
        # Show current pool status
        pool_info = {
            "pool_config": connection.settings_dict.get('OPTIONS', {}).get('pool', {}),
            "connection_vendor": connection.vendor,
        }

        # Run stress test
        start_time = time.time()
        thread_results = create_multiple_connections()
        end_time = time.time()

        # Try a long-running query that might cause issues
        long_query_result = long_running_query()

        return JsonResponse({
            "message": "Connection pool stress test completed",
            "pool_info": pool_info,
            "execution_time": f"{end_time - start_time:.2f} seconds",
            "thread_results": thread_results,
            "long_query_result": long_query_result,
            "total_threads": len(thread_results),
            "errors": [r for r in thread_results if "ERROR" in r]
        }, json_dumps_params={'indent': 2})

    except Exception as e:
        sentry_sdk.capture_exception(e)
        return JsonResponse({
            "error": "Connection pool stress test failed",
            "message": str(e),
            "pool_info": pool_info if 'pool_info' in locals() else "Unknown"
        }, status=500)


def sentry_database_interaction_test(request):
    """Test how Sentry SDK interacts with database operations"""
    import time

    try:
        # Simulate multiple database operations with Sentry tracking
        start_time = time.time()

        # 1. Create a new greeting (write operation)
        new_greeting = Greeting.objects.create(
            message=f"Test greeting at {time.time()}",
            count=1
        )

        # 2. Trigger Sentry span for database operation
        with sentry_sdk.start_span(op="db.query", description="Get all greetings"):
            greetings = list(Greeting.objects.all())

        # 3. Update operation
        with sentry_sdk.start_span(op="db.query", description="Update greeting count"):
            new_greeting.count += 1
            new_greeting.save()

        # 4. Complex query with Sentry span
        with sentry_sdk.start_span(op="db.query", description="Complex aggregation"):
            from django.db.models import Avg, Count, Max
            stats = Greeting.objects.aggregate(
                avg_count=Avg('count'),
                total_greetings=Count('id'),
                max_count=Max('count')
            )

        # 5. Delete the test greeting
        with sentry_sdk.start_span(op="db.query", description="Delete test greeting"):
            new_greeting.delete()

        end_time = time.time()

        return JsonResponse({
            "message": "Sentry database interaction test completed",
            "execution_time": f"{end_time - start_time:.2f} seconds",
            "operations_performed": [
                "CREATE greeting",
                "SELECT all greetings",
                "UPDATE greeting count",
                "AGGREGATE statistics",
                "DELETE test greeting"
            ],
            "statistics": stats,
            "total_greetings": len(greetings),
            "sentry_spans_created": 4
        }, json_dumps_params={'indent': 2})

    except Exception as e:
        sentry_sdk.capture_exception(e)
        return JsonResponse({
            "error": "Sentry database interaction test failed",
            "message": str(e)
        }, status=500)


def connection_leak_simulation(request):
    """Simulate potential connection leaks that could starve the pool"""
    import time
    from django.db import connection

    try:
        connections_info = []

        # Try to exhaust the connection pool
        for i in range(12):  # More than our max_size of 10
            try:
                start_time = time.time()

                # Force a new connection by doing a raw query
                with connection.cursor() as cursor:
                    cursor.execute("SELECT pg_backend_pid(), now();")
                    backend_pid, current_time = cursor.fetchone()

                connections_info.append({
                    "attempt": i + 1,
                    "backend_pid": backend_pid,
                    "time": current_time.isoformat(),
                    "duration": f"{time.time() - start_time:.3f}s"
                })

                # Simulate work that holds the connection
                time.sleep(0.5)

            except Exception as e:
                connections_info.append({
                    "attempt": i + 1,
                    "error": str(e),
                    "duration": f"{time.time() - start_time:.3f}s"
                })

        return JsonResponse({
            "message": "Connection leak simulation completed",
            "pool_max_size": connection.settings_dict.get('OPTIONS', {}).get('pool', {}).get('max_size', 'unknown'),
            "attempts": len(connections_info),
            "connections_info": connections_info,
            "errors": [info for info in connections_info if 'error' in info]
        }, json_dumps_params={'indent': 2})

    except Exception as e:
        sentry_sdk.capture_exception(e)
        return JsonResponse({
            "error": "Connection leak simulation failed",
            "message": str(e)
        }, status=500)
