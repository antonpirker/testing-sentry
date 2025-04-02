import os
from decimal import BasicContext, FloatOperation, Inexact, setcontext

from fastapi import FastAPI

import sentry_sdk

sentry_sdk.init(
    dsn=os.environ.get("SENTRY_DSN"),
    environment=os.environ.get("ENV", "test"),
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
    debug=True,
)

def decimal_setup() -> None:
    BasicContext.traps[Inexact] = True
    BasicContext.traps[FloatOperation] = True
    setcontext(BasicContext)



decimal_setup()


app = FastAPI()


@app.get("/")
def endpoint():
    return {
        "hello": "world!",
        "errors-are-here": "http://localhost:5000/error",
    }


@app.get("/error")
def endpoint():
    raise ValueError("help! an error!")
