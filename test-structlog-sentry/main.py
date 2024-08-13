import logging
import os

import sentry_sdk
import structlog
from structlog_sentry import SentryProcessor


def main():
    sentry_sdk.init(
        dsn=os.environ.get("SENTRY_DSN"),
        traces_sample_rate=1.0,
        debug=True,
    )

    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.stdlib.add_logger_name,  # optional, must be placed before SentryProcessor()
            structlog.stdlib.add_log_level,  # required before SentryProcessor()
            SentryProcessor(event_level=logging.ERROR),
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
    )

    log = structlog.get_logger()

    try:
        1/0
    except ZeroDivisionError:
        log.error("zero division")


if __name__ == "__main__":
    main()