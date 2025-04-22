from fastapi import FastAPI, Depends
import os

import sentry_sdk
sentry_sdk.init(
    dsn=os.environ.get("SENTRY_DSN"),
    environment=os.environ.get("ENV", "fastapi"),
    release=os.environ.get("RELEASE", "fastapi@0.0.1a"),
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
    debug=True,
)


app = FastAPI()


def get_user():
    user = {
      "id": "testuser",
      "username": "Test User",
    }
    sentry_sdk.set_user(user)
    return user


@app.middleware("http")
async def test_middleware(request, call_next):
    print("middleware")
    return await call_next(request)


@app.get("/error")
def error(user=Depends(get_user)):
    with sentry_sdk.start_span(name="test-span"):
        with sentry_sdk.start_span(name="test-span-2") as span:
            # tag
            sentry_sdk.set_tag("test-tag", "test-value")

            # user
            sentry_sdk.set_user(user)

            # breadcrumb
            sentry_sdk.add_breadcrumb(
                category="test-category",
                message="test breadcrumb",
                level="info",
                data={"user": user},
            )

            # context
            sentry_sdk.set_context("test-context", {"text-context-user": user})

            # attachment
            scope = sentry_sdk.get_current_scope()
            scope.add_attachment(bytes=b"Hello World", filename="hello.txt")

            raise ValueError("help! an error!")


@app.get("/")
def index():
    return {
        "hello": "world!",
        "errors-are-here": "http://localhost:5000/error",
    }
