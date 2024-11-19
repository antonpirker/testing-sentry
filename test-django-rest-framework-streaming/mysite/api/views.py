from rest_framework.views import APIView

from django.http import StreamingHttpResponse, HttpResponse

import sentry_sdk

import time

# TODO: print process id in both places and check if it the same
# TODO: try with one worker setting in gunicorn call site


def generate_response():
    print(f"2 GENERATOR contextvar _current_scope {sentry_sdk.scope._current_scope}")
    print(f"2 GENERATOR contextvar _current_scope value {sentry_sdk.scope._current_scope.get()}")
    print(f"2 GENERATOR current: {sentry_sdk.get_current_scope()}")
    print(f"2 GENERATOR span on current: {sentry_sdk.get_current_scope().span}")
    print(f"2 GENERATOR propagation context current: {sentry_sdk.get_current_scope()._propagation_context}")
    with sentry_sdk.start_span(description="SPAN Stream Response Generator", op="demo.function") as span:
        print(f"SPAN START generator: {span}")
        span.set_data("more", "value")
        for i in range(3):
            with sentry_sdk.start_span(description="Stream Chunk", op="demo.function") as span2:
                print(f"SPAN START chunk: {span2}")
                time.sleep(0.2)
                yield f"Hello, {i} World!\n"

            print(f"SPAN END chunk: {span2.start_timestamp} -> {span2.timestamp} ({span2.timestamp - span2.start_timestamp})")

    print(f"SPAN END generator: {span.start_timestamp} -> {span.timestamp} ({span.timestamp - span.start_timestamp})")

class DemoView(APIView):
    def get(self, request):
        print(f"1 VIEW contextvar _current_scope {sentry_sdk.scope._current_scope}")
        print(f"1 VIEW contextvar _current_scope value {sentry_sdk.scope._current_scope.get()}")
        print(f"1 VIEW current: {sentry_sdk.get_current_scope()}")
        print(f"1 VIEW span on current: {sentry_sdk.get_current_scope().span}")
        print(f"1 VIEW propagation context current: {sentry_sdk.get_current_scope()._propagation_context}")

        with sentry_sdk.start_span(description="SPAN Streaming View", op="demo.function") as span:
            print(f"SPAN START view: {span}")
            span.set_data("some", "value")
            print(span)
            with sentry_sdk.
            output = StreamingHttpResponse(generate_response(), content_type="text/plain")

        print(f"SPAN END view: {span.start_timestamp} -> {span.timestamp} ({span.timestamp - span.start_timestamp})")
        return output

class DemoView2(APIView):
    def get(self, request):
        return HttpResponse("Hello, World!\n")