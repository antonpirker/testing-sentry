import os

from fastapi import FastAPI, Depends

from starlette.types import Receive, Scope, Send
from starlette.middleware import Middleware

import sentry_sdk

sentry_sdk.init(
    dsn=os.environ.get("SENTRY_DSN"),
    environment=os.environ.get("ENV", "test"),
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
    # debug=True,
)


class LoggingMiddleware:
    def __init__(
        self,
        *args,
        **kwargs,
    ) -> None:
        self.name = args[0]
    
    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        ...


app = FastAPI(
    middleware=[
        Middleware(LoggingMiddleware, "app.request"),
    ],
)


def get_user():
    user = {
      "id": "testuser"
    }
    sentry_sdk.set_user(user)
    return user


@app.middleware("http")
async def test_middleware(request, call_next):
    print("middleware")
    return await call_next(request)


@app.get("/error")
def endpoint(user = Depends(get_user)):
    raise ValueError("help! an error!")


@app.get("/")
def endpoint():
    return {
        "hello": "world!",
        "errors-are-here": "http://localhost:5000/error",
    }
