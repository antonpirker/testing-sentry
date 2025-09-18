import asyncio
import os

import sentry_sdk

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
)


async def main():
    sentry_sdk.init(
        dsn=os.getenv("SENTRY_DSN", None),
        environment=os.getenv("ENV", "local"),
        traces_sample_rate=1.0,
        send_default_pii=True,
        enable_logs=True,
        debug=True,
    )

    with sentry_sdk.start_transaction(op="function", name="logs-tags-transaction"):
        outcome = ValueError("test error")

        extra = {
            "one": "1",
        }
        tags = {
            "interaction_type": "proxy_request",
        }
        sentry_sdk.set_tags(tags)

        extra.update(tags)
        log_params = {
            "extra": extra,
        }
        event_id = sentry_sdk.capture_exception(outcome) # error event sent
        log_params["extra"]["slo_event_id"] = event_id

        logger.warning("something", **log_params) # log event sent`


if __name__ == "__main__":
    asyncio.run(main())
