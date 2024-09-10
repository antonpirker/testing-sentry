import os
from random import random

import sentry_sdk
from sentry_sdk.types import Event, Hint


def error_sampler(event: Event, hint: Hint) -> float:   
    error_class = hint["exc_info"][0]
    
    if error_class == NotImplementedError:
        print("Ignoring NotImplementedError!")
        return 0
    
    # All the other errors
    return 1.0


sentry_sdk.init(
    dsn=os.environ["SENTRY_DSN"],
    enable_tracing=True,
    debug=True,
    error_sampler=error_sampler,
)

if random() > 0.5:
    raise NotImplementedError("We will do this in the future")

else:
    raise ValueError("This is a test error")