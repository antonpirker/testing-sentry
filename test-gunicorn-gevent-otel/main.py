import sentry_sdk

from opentelemetry import trace
tracer = trace.get_tracer(__name__)


def application(environ, start_fn):
    """
    That's the WSGI application
    """
    # Using OpenTelementry to instrument
    with tracer.start_as_current_span("test_otel_span"):
        start_fn('200 OK', [('Content-Type', 'text/plain')])
        return [b"Hello World!\n", str(environ).encode('utf-8')]

    # # Using Sentry SDK to instrument
    # # (you need to remove `instrumenter="otel"` from the Sentry SDK initialization in gunicorn.conf.py)
    # with sentry_sdk.start_transaction(op="gunicorn-main", name="My Transaction"):
    #     start_fn('200 OK', [('Content-Type', 'text/plain')])
    #     return [b"Hello World!\n", str(environ).encode('utf-8')]
