import os
import threading

import sentry_sdk



@sentry_sdk.tracing.trace
def my_function():
    print("Function: starting")
    ...


def thread_function():
    print("Thread: starting")
    my_function()


if __name__ == "__main__":
    print("Main: starting")
    sentry_sdk.init(
        dsn=os.environ.get("SENTRY_DSN"),
        environment=os.environ.get("ENV", "test"),
        # Set rate to 1.0 to capture 100%
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
        debug=True,
    )   

    with sentry_sdk.start_transaction(op="transaction", name="main-transaction"):
        t1 = threading.Thread(target=thread_function, daemon=True)   
        t1.start()
        t1.join()

    print("Main: all done")
