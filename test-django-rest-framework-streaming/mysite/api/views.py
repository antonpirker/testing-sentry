from rest_framework.views import APIView
from rest_framework.response import Response

from django.http import StreamingHttpResponse

import sentry_sdk

import threading


def generate_response():
    print("===")
    print(f"~~~~~~~~~~~ _current_scope {sentry_sdk.scope._current_scope}")
    print(f"~~~~~~~~~~~ _current_scope.get {sentry_sdk.scope._current_scope.get()}")
    print(f"2 GENERATOR current: {sentry_sdk.get_current_scope()}")
    print(f"2 GENERATOR span on current: {sentry_sdk.get_current_scope().span}")
    print(f"2 GENERATOR propagation context current: {sentry_sdk.get_current_scope()._propagation_context}")
    with sentry_sdk.start_span(name="SPAN Stream Response Generator", op="demo.function") as span:
        span.set_data("more", "value") 
        print("---")
        print(span)
        for i in range(10):
            with sentry_sdk.start_span(name="Stream Chunk", op="demo.function") as span:
                span.set_data("my chunk", i)
                yield f"Hello, {i} World!\n"


class DemoView(APIView):
    def get(self, request):
        print("===")
        print(f"~~~~~~~~~~~ _current_scope {sentry_sdk.scope._current_scope}")
        print(f"~~~~~~~~~~~ _current_scope get {sentry_sdk.scope._current_scope.get()}")
        print(f"1 VIEW current: {sentry_sdk.get_current_scope()}")
        print(f"1 VIEW span on current: {sentry_sdk.get_current_scope().span}")
        print(f"1 VIEW propagation context current: {sentry_sdk.get_current_scope()._propagation_context}")

        with sentry_sdk.start_span(name="SPAN Streaming View", op="demo.function") as span:
            span.set_data("some", "value") 
            print("---")
            print(span)
            return StreamingHttpResponse(generate_response(), content_type="text/plain")