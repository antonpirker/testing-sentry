from django.http import JsonResponse
from django.shortcuts import render


import sentry_sdk


def api(request):
    data = {
        "message": "New JSON response",
        "polls": [
            {
                "id": 1,
                "question": "Do you like Summer?",
                "votes": 100
            },
            {
                "id": 2,
                "question": "Do you like Winter?",
                "votes": 200
            }
        ]
    }
    return JsonResponse(data)


def index(request):
    # Render Sentry trace information as meta tags
    # This is done to propagate the trace information from the backend to the frontend
    meta = ""
    meta += '<meta name="sentry-trace" content="%s">' % sentry_sdk.get_traceparent()
    meta += '<meta name="baggage" content="%s">' % sentry_sdk.get_baggage()

    return render(request, 'polls/index.html', {
        'additional_meta': meta,
        'message': "Hello, world. You're at the polls index."
    })
