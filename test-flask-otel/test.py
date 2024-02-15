import time
import os

import sentry_sdk
from opentelemetry import trace
from opentelemetry.propagate import set_global_textmap
from opentelemetry.sdk.trace import TracerProvider
from sentry_sdk.integrations.opentelemetry import SentryPropagator, SentrySpanProcessor

sentry_sdk.init(
    dsn=os.environ["SENTRY_DSN"],
    enable_tracing=True,
    instrumenter="otel",
    _experiments={
        "otel_powered_performance": True, 
    },
    debug=True,
)

provider = TracerProvider()
provider.add_span_processor(SentrySpanProcessor())
trace.set_tracer_provider(provider)
set_global_textmap(SentryPropagator())

tracer = trace.get_tracer(__name__)

# Start a new span
with tracer.start_as_current_span("test_otel_span"):
    with tracer.start_as_current_span("test_otel_span_child"):
        print("Processing some data...")
    # Simulate some processing
    time.sleep(1)
