import os

import ray

from sentry_sdk.integrations.ray import RayIntegration
import sentry_sdk


def init_sentry():
    sentry_sdk.init(
        dsn=os.environ.get("SENTRY_DSN"),
        traces_sample_rate=1.0,
        debug=True,
        integrations=[
            RayIntegration(),
        ],
    )


if __name__ == "__main__":
    init_sentry()

    ray.init(
        runtime_env=dict(worker_process_setup_hook=init_sentry), 
    )

    # Does work: tasks as functions
    @ray.remote
    def my_cool_task(a, b, c):
        with sentry_sdk.start_span(description="big-processing"):
            return a + b + c

    @ray.remote
    def my_failing_task(a, b, c):
        with sentry_sdk.start_span(description="big-processing"):
            return a/b/c

    with sentry_sdk.start_transaction(name="ray-test"):
        futures = [
            my_cool_task.remote(1, 2, 3),
            my_failing_task.remote(2, 1, 0),
        ]
        result = ray.get(futures)
        print(f"Result: {result}")


    # Does NOT work: Actors (class based tasks) are not supported yet.
    @ray.remote
    class Counter(object):
        def __init__(self):
            self.n = 0

        def increment(self):
            self.n += 1

        def decrement(self):
            raise NotImplementedError("There is no decrement in a counter!")

        def read(self):
            return self.n

    with sentry_sdk.start_transaction(name="ray-test"):
        counter = Counter.remote()

        # The errors are captured, but 
        # tracing information is not sent to Sentry
        futures = [
            counter.increment.remote(), 
            counter.decrement.remote(), 
        ]
        result = ray.get(futures)
        print(f"Result: {result}")
