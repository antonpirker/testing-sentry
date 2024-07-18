from fastapi import FastAPI
import os

import sentry_sdk

sentry_sdk.init(
    dsn=os.environ.get("SENTRY_DSN"),
    environment=os.environ.get("ENV", "test"),
    # Set rate to 1.0 to capture 100%
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
    debug=True,
)


app = FastAPI()

@app.middleware("http")
async def test_middleware(request, call_next):
    print("middleware")
    return await call_next(request)


@app.get("/error")
def endpoint():
    raise ValueError("help! an error!")


@app.get("/")
def endpoint():
    return {
        "hello": "world!",
        "errors-are-here": "http://localhost:5000/error",
    }
