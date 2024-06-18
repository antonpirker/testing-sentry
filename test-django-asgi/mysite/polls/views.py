from django.http import HttpResponse

import sentry_sdk

async def index(request):
    sentry_sdk.capture_message("Hello from Django!")
    return HttpResponse("Hello, world.")
