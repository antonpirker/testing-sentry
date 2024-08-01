import os
import time

from litestar import Litestar, get
from litestar.logging.config import LoggingConfig
from litestar.middleware.logging import LoggingMiddlewareConfig
from litestar.middleware.rate_limit import RateLimitConfig
from litestar.middleware.session.client_side import CookieBackendConfig


from sentry_sdk.integrations.litestar import LitestarIntegration
import sentry_sdk


sentry_sdk.init(
    dsn=os.environ.get("SENTRY_DSN"),
    enable_tracing=True,
    debug=True,
    integrations=[
        LitestarIntegration(),
    ],
)


@get("/")
async def index() -> str:
    return "Hello, world!"


@get("/error")
async def error() -> dict[str, int]:
    var1 = 123
    var2 = 0
    bla = var1 / var2
    return {"error": bla}


@get("/books/{book_id:int}")
async def get_book(book_id: int) -> dict[str, int]:
    time.sleep(0.2)
    return {"book_id": book_id}


logging_middleware_config = LoggingMiddlewareConfig()
rate_limit_config = RateLimitConfig(rate_limit=("second", 1), exclude=["/schema"])
session_config = CookieBackendConfig(secret=os.urandom(16))  # type: ignore[arg-type]


app = Litestar(
    route_handlers=[index, get_book, error], 
    logging_config=LoggingConfig(),
    middleware=[
        logging_middleware_config.middleware, 
        rate_limit_config.middleware, 
        session_config.middleware,
    ],
)
