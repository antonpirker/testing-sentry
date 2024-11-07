from rest_framework.views import APIView
from rest_framework.response import Response

from django.http import StreamingHttpResponse

import sentry_sdk


def generate_response():
    with sentry_sdk.start_span(name="Stream Response Generator", op="demo.function") as span:
        span.set_data("more", "value") 
        for i in range(10):
            yield f"Hello, {i} World!\n"


class DemoView(APIView):
    def get(self, request):
        with sentry_sdk.start_span(name="Streaming View", op="demo.function") as span:
            span.set_data("some", "value") 
            return StreamingHttpResponse(generate_response(), content_type="text/plain")