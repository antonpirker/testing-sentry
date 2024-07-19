import logging
import os
import time

import sentry_sdk
from fastapi import FastAPI, Request, Response
from starlette.middleware import Middleware
from starlette.middleware.base import (
    BaseHTTPMiddleware,
    DispatchFunction,
    RequestResponseEndpoint,
)
from starlette.types import ASGIApp


class RequestLoggerMiddleware(BaseHTTPMiddleware):
    def __init__(
        self, logger_name: str, app: ASGIApp, dispatch: DispatchFunction | None = None
    ):
        super().__init__(app, dispatch)
        self.logger = logging.getLogger(logger_name)

    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        self.logger.info("Request open")

        start_time = time.time()
        response = await call_next(request)
        duration = time.time() - start_time

        self.logger.info(f"Request close {duration=}")
        return response

if os.environ.get("SENTRY"):
    sentry_sdk.init()

logging.basicConfig(level=logging.INFO)

app = FastAPI(
    middleware=[
        Middleware(RequestLoggerMiddleware, "app.request"),
    ],
)


@app.get("/")
def hello() -> str:
    return "Hello World!"