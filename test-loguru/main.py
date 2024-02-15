import sys
import logging

from loguru import logger as loguru_logger
# loguru_logger.remove()
# loguru_logger.add(sys.stdout, backtrace=True, diagnose=True)  # Caution, may leak sensitive data in prod


import sentry_sdk
import sentry_sdk.integrations.loguru
sentry_sdk.init(
    dsn="https://229ebb4a2d1043fc93de7290365200ec@o447951.ingest.sentry.io/4505079351279616",
    integrations=[
        sentry_sdk.integrations.loguru.LoguruIntegration(),
    ],
    traces_sample_rate=1.0, 
    debug=True,
)


@loguru_logger.catch
def my_function(x, y, z):
    # An error? It's caught anyway!
    return 1 / (x + y + z)


def main():
    loguru_logger.debug("Guru: I am ignored")
    loguru_logger.info("Guru: I am a breadcrumb")
    loguru_logger.error("Guru: I am an event", extra=dict(bar=43))

    try:
        1 / 0
    except ZeroDivisionError:
        loguru_logger.exception("Guru: An exception XXX happened")
    

    # logging.debug("I am ignored")
    # logging.info("I am a breadcrumb")
    # logging.error("I am an event", extra=dict(bar=43))
    # logging.exception("An exception happened")    

    # my_function()


if __name__ == "__main__":
    main()