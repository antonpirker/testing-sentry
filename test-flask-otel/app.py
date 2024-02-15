import logging
import os
from random import randint

from flask import Flask, request

from opentelemetry import trace
from opentelemetry.propagate import set_global_textmap

import sentry_sdk
from sentry_sdk.integrations.opentelemetry import SentrySpanProcessor, SentryPropagator


sentry_sdk.init(
    dsn=os.environ["SENTRY_DSN"],
    enable_tracing=True,
    # set the instrumenter to use OpenTelemetry instead of Sentry
    instrumenter="otel",
    debug=True,
)

provider = trace.get_tracer_provider()
provider.add_span_processor(SentrySpanProcessor())
set_global_textmap(SentryPropagator())

# Acquire a tracer
tracer = trace.get_tracer("diceroller.tracer")

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.route("/rolldice")
def roll_dice():
    player = request.args.get("player", default=None, type=str)
    result = str(roll())
    if player:
        logger.warn("%s is rolling the dice: %s", player, result)
    else:
        logger.warn("Anonymous player is rolling the dice: %s", result)
    return result


def roll():
    # This creates a new span that's the child of the current one
    with tracer.start_as_current_span("roll") as rollspan:
        res = randint(1, 6)
        rollspan.set_attribute("roll.value", res)
        return res
