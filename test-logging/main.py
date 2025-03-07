import asyncio
import os

import sentry_sdk

import logging
logger = logging.getLogger()
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s')


async def main():
    sentry_sdk.init(
        dsn=os.getenv("SENTRY_DSN", None),
        environment=os.getenv("ENV", "local"),
        traces_sample_rate=1.0,
        send_default_pii=True,
        debug=True,

    )

    string_value = "SomeStringValue"
    non_string_value = 42
    none_value = None


    with sentry_sdk.start_transaction(op="function", name="logging-transaction"):
        # logger.warning("warn1 %s", "None")
        logger.warning("warnXX %s", None)
        # logger.warning("warn3 %s", 3)

        # logger.error("error1 %s", "None")
        logger.error("errorXX %s", None)
        # logger.error("error3 %s", 3)

        # logger.debug("I am ignored [%s] [%s] [%s]", string_value, non_string_value, none_value)
        # logger.info("I am a breadcrumb [%s] [%s] [%s]", string_value, non_string_value, none_value)
        # logger.error("I am an event [%s] [%s] [%s]", string_value, non_string_value, none_value)
        # logger.exception("An exception happened [%s] [%s] [%s]", string_value, non_string_value, none_value)

        # logger.debug(f"[f-string] I am ignored [{string_value}] [{non_string_value}] [{none_value}]")
        # logger.info(f"[f-string] I am a breadcrumb [{string_value}] [{non_string_value}] [{none_value}]")
        # logger.error(f"[f-string] I am an event [{string_value}] [{non_string_value}] [{none_value}]")
        # logger.exception(f"[f-string] An exception happened [{string_value}] [{non_string_value}] [{none_value}]")


if __name__ == "__main__":
    asyncio.run(main())