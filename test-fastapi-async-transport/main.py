from fastapi import FastAPI, Depends, HTTPException
import os
from contextlib import asynccontextmanager

import sentry_sdk
from sentry_sdk.integrations.starlette import StarletteIntegration
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.asyncio import AsyncioIntegration

failed_request_status_codes = [range(400, 600)]


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan with proper Sentry cleanup."""
    print(":rocket: Starting FastAPI with Sentry async transport...")
    sentry_sdk.init(
        dsn=os.environ.get("SENTRY_DSN"),
        environment=os.environ.get("ENV", "test"),
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
        release="1.0.0",
        debug=True,
        _experiments={
            "transport_async": True,
        },
        # FastAPI integration
        integrations=[
            StarletteIntegration(),
            FastApiIntegration(),
            AsyncioIntegration(),
        ],
    )
    # Verify transport type
    client = sentry_sdk.get_client()
    transport_name = type(client.transport).__name__ if client.transport else "None"
    print(f":white_check_mark: Sentry initialized with {transport_name}")

    yield

app = FastAPI(lifespan=lifespan)


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


@app.post("/post")
def main(user):
    return user


@app.get("/")
def endpoint():
    return {
        "hello": "world!",
        "errors-are-here": "http://localhost:5000/error",
        "http-exception": "http://localhost:5000/http-exception",
    }
