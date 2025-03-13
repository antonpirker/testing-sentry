import os

import sentry_sdk
from sentry_sdk.integrations.wsgi import SentryWsgiMiddleware

sentry_sdk.init(
    dsn=os.environ.get("SENTRY_DSN"),
    environment=os.environ.get("ENV", "test"),
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
    debug=True,
)

def fibonacci(n):
    if n < 0:
        print("Incorrect input")
    elif n == 0:
        return 0
    elif n == 1 or n == 2:
        return 1
    else:
        return fibonacci(n-1) + fibonacci(n-2)


# Simple WSGI application
def simple_app(environ, start_response):
    """A simple WSGI application"""
    path = environ.get('PATH_INFO', '').lstrip('/')
    
    if path == '':
        # Root path
        status = '200 OK'
        headers = [('Content-type', 'text/plain')]
        start_response(status, headers)
        fibonacci(30)
        return [b'Hello, World!']
    
    elif path == 'error':
        # Deliberately raise an error for Sentry testing
        try:
            raise Exception("This is a test error for Sentry")
        except Exception as e:
            status = '500 Internal Server Error'
            headers = [('Content-type', 'text/plain')]
            start_response(status, headers)
            return [b'An error occurred']
        
    else:
        # 404 for any other path
        status = '404 Not Found'
        headers = [('Content-type', 'text/plain')]
        start_response(status, headers)
        return [b'Not Found']

# Wrap the WSGI app with Sentry middleware
app = SentryWsgiMiddleware(simple_app)


# For running directly
if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    httpd = make_server('', 8000, app)
    print("Serving on port 8000...")
    httpd.serve_forever()

