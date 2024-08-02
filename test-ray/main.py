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

    # function tasks work

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


    # Actors (class based tasks) do not work   
    
    @ray.remote
    class Counter(object):
        def __init__(self):
            self.n = 0

        def increment(self):
            self.n += 1

        def read(self):
            return self.n

    # function tasks work
    with sentry_sdk.start_transaction(name="ray-test"):
        # counter is of type `ray._raylet.ObjectRef`
        # instead of the correct `ray._raylet.ActorHandle)`  
        # when sentry.init() is called with the RayIntegration
        counter = Counter.remote()
        
        future = counter.increment.remote()
        result = ray.get(futures)
        print(f"Result: {result}")
