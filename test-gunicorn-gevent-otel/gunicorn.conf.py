import os

bind = "0.0.0.0:8080"
wsgi_app = "main"

worker_class = "gevent"
workers = 2
worker_connections = 1000
max_requests = 25
preload_app = False

reload = True
loglevel = "debug"
errorlog = "-"
accesslog = "-"


def post_fork(server, worker):
    print(f"*** post_fork {server} / {worker}")
    # If Sentry SDK is initialized here, I get the "Monkey-patching ssl after ssl has already been imported may lead to errors" error during the worker init


def post_worker_init(worker):
    print(f"*** post_worker_init {worker}")

    # Initialize OpenTelementry
    from opentelemetry import trace
    from opentelemetry.propagate import set_global_textmap
    from opentelemetry.sdk.trace import TracerProvider
    from sentry_sdk.integrations.opentelemetry import SentrySpanProcessor, SentryPropagator

    provider = TracerProvider()
    provider.add_span_processor(SentrySpanProcessor())
    trace.set_tracer_provider(provider)
    set_global_textmap(SentryPropagator())

    # Initialize Sentry SDK
    import sentry_sdk
    sentry_sdk.init(
        dsn=os.environ["SENTRY_DSN"],
        traces_sample_rate=1.0,
        debug=True,
        instrumenter="otel",
    )
