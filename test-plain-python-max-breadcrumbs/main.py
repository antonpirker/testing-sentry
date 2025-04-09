import asyncio
import logging
import os

import sentry_sdk


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


async def main():
    sentry_sdk.init(
        dsn=os.getenv("SENTRY_DSN", None),
        environment=os.getenv("ENV", "local"),
        traces_sample_rate=1.0,
        debug=True,
        max_breadcrumbs=3,
    )

    with sentry_sdk.start_transaction(op="function", name="test-transaction"):
        logger.info("breadcrumb 1", extra=dict(foo=42, password="secret"))
        logger.info("breadcrumb 2", extra=dict(foo=1, password="secret"))
        logger.info("breadcrumb 3", extra=dict(bar=2, auth="secret"))
        logger.info("breadcrumb 4", extra=dict(foobar=3, password="secret"))
        logger.info("breadcrumb 5", extra=dict(foobar=45, password="secret"))
        # only the last 3 breadcrumbs are sent
        logger.critical("whoops", extra=dict(bar=69, auth="secret"))


if __name__ == "__main__":
    asyncio.run(main())
