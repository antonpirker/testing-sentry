import os

import sentry_sdk
from sentry_sdk.integrations.starlette import StarletteIntegration

from fastapi import FastAPI
from fastapi.responses import StreamingResponse


sentry_sdk.init(
    dsn=os.environ.get("SENTRY_DSN"),
    traces_sample_rate=1.0,
    integrations=[
        StarletteIntegration(middleware_spans=False),
    ],
    debug=True,
)

app = FastAPI()


def generate_response():
    with sentry_sdk.start_span(description="SPAN Stream Response Generator", op="demo.function") as span:
        print(f"SPAN START generator: {span}")
        span.set_data("more", "value")
        for i in range(3):
            with sentry_sdk.start_span(description="Stream Chunk", op="demo.function") as span2:
                print(f"SPAN START chunk: {span2}")
                yield f"Hello, {i} World!\n"

            print(f"SPAN END chunk: {span2.start_timestamp} -> {span2.timestamp}")

    print(f"SPAN END generator: {span.start_timestamp} -> {span.timestamp}")


@app.get("/")
def hello() -> str:
    with sentry_sdk.start_span(description="SPAN Streaming View", op="demo.function") as span:
        print(f"SPAN START view: {span}")
        span.set_data("some", "value")
        print(span)
        output = StreamingResponse(generate_response(), media_type='text/event-stream')

    print(f"SPAN END view: {span.start_timestamp} -> {span.timestamp}")
    return output
