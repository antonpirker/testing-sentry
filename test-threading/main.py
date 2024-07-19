import os
import random
import threading
import time

import sentry_sdk


@sentry_sdk.tracing.trace
def my_function(id):
    print("Function: starting")
    time.sleep(random.randint(0,3))
    sentry_sdk.add_breadcrumb(message=f"my_function({id}): doing something", category="function", level="info")
    

def thread_function(id):
    print("Thread: starting")
    time.sleep(random.randint(0,2))
    sentry_sdk.add_breadcrumb(message=f"thread_function({id}): doing something", category="function", level="info")
    my_function(id)


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
        sentry_sdk.add_breadcrumb(message=f"main(): starting threads", category="function", level="info")
        threads = []

        for i in range(5):
            t = threading.Thread(target=thread_function, name=f"mythread{i}", args=(i, ), daemon=True)   
            threads.append(t)

            t.start()
            sentry_sdk.add_breadcrumb(message=f"main(): thread {i} started", category="function", level="info")

        for t in threads:
            t.join()
            sentry_sdk.add_breadcrumb(message=f"main(): thread {t} joined", category="function", level="info")

        sentry_sdk.add_breadcrumb(message=f"main(): all threads joined", category="function", level="info")

    raise ValueError("Last minute error")
    print("Main: all done")
