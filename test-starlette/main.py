import os

from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

import sentry_sdk


sentry_sdk.init(
    dsn=os.environ.get("SENTRY_DSN"),
    enable_tracing=True,
    debug=True,
)


async def homepage(request):
    return JSONResponse({'hello': 'world'})


app = Starlette(debug=True, routes=[
    Route('/', homepage),
])