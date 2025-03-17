import os
import random

import sentry_sdk

from sentry_sdk import _experimental_logger as sentry_logger


def before_log(record, hint):
    print("before_log record", record)
    print("before_log hint", hint)

    if record['severity_text'] == 'fatal':
        return None
    
    return record


sentry_sdk.init(
    dsn=os.environ.get("SENTRY_DSN"),
    environment=os.environ.get("ENV", "test"),
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
    debug=True,
    enable_sentry_logs=True,
    before_emit_log=before_log,
)


def main():
    for x in range(1000):
        sentry_logger.trace("This is a 'trace' log...{rand}", rand=random.randint(0, 100)) 
        sentry_logger.debug("This is a 'debug' log... ({rand})", rand=random.randint(0, 100), bla="asdfoamsdfl") 
        sentry_logger.info("This is a 'info' log... ({rand})", rand=random.randint(0, 100)) 
        sentry_logger.warn("This is a 'warn' log... ({rand})", rand=random.randint(0, 100)) 
        sentry_logger.error("This is a 'error' log... ({rand})", rand=random.randint(0, 100)) 
        sentry_logger.fatal("This is a 'fatal' log... ({rand})", rand=random.randint(0, 100)) 


# For running directly
if __name__ == '__main__':
    main()