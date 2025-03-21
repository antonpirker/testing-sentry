import asyncio
import os

import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration

import logging
logger = logging.getLogger()
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(message)s',
)


async def main():
    sentry_sdk.init(
        dsn=os.getenv("SENTRY_DSN", None),
        environment=os.getenv("ENV", "local"),
        integrations=[
            LoggingIntegration(
                level=logging.DEBUG,
                event_level=logging.ERROR,
            ),
        ],
        _experiments={
            "enable_sentry_logs": True,
        },
        traces_sample_rate=1.0,
        send_default_pii=True,
        debug=True,
    )

    my_value = "SomeStringValue"

    with sentry_sdk.start_transaction(op="function", name="logging-transaction"):
        logger.debug("Using python.logging.debug, my_value: %s", my_value)
        logger.info("Using python.logging.info, my_value: %s", my_value)
        logger.warning("Using python.logging.warning, my_value: %s", my_value)
        logger.error("Using python.logging.error, my_value: %s", my_value)
        logger.critical("Using python.logging.critical, my_value: %s", my_value)
        logger.exception("Using python.logging.exception, my_value: %s", my_value)

        logger.debug(f"Using python.logging.debug with f-string, my_value: {my_value}")
        logger.info(f"Using python.logging.info with f-string, my_value: {my_value}")
        logger.warning(f"Using python.logging.warning with f-string, my_value: {my_value}")
        logger.error(f"Using python.logging.error with f-string, my_value: {my_value}")
        logger.critical(f"Using python.logging.critical with f-string, my_value: {my_value}")
        logger.exception(f"Using python.logging.exception with f-string, my_value: {my_value}")


if __name__ == "__main__":
    asyncio.run(main())
