import os
import time
import threading

from rest_framework.views import APIView

from django.http import StreamingHttpResponse, HttpResponse

import sentry_sdk


def generate_response():
    print(f"2 GENERATOR PID {os.getpid()} / thread: {threading.get_ident()}")
    print(f"2 GENERATOR current scope: {sentry_sdk.get_current_scope()} (span: {sentry_sdk.get_current_scope().span})")

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
        print(f"1 VIEW PID {os.getpid()} / thread: {threading.get_ident()}")
        print(f"1 VIEW current scope: {sentry_sdk.get_current_scope()} (span: {sentry_sdk.get_current_scope().span})")

        with sentry_sdk.start_span(description="SPAN Streaming View", op="demo.function") as span:
            print(f"SPAN START view: {span}")
            span.set_data("some", "value")
            print(span)
            output = StreamingHttpResponse(generate_response(), content_type="text/plain")

        print(f"SPAN END view: {span.start_timestamp} -> {span.timestamp} ({span.timestamp - span.start_timestamp})")
        return output


class DemoView2(APIView):
    def get(self, request):
        return HttpResponse("Hello, World!\n")
