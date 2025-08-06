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
