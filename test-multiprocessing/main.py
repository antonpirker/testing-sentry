import multiprocessing
import os
import time

import sentry_sdk


def _check_workers(workers):
    if any([worker.exitcode != 0 for worker in workers]):
        raise Exception("Hanging with this error x")


def wait_for_processes(workers, sleep_seconds=5):
    while any([worker.is_alive() for worker in workers]):
        _check_workers(workers=workers)

        time.sleep(sleep_seconds)

    _check_workers(workers=workers)


def failing_function():
    raise ValueError("Test error x")


def execute():
    manager = multiprocessing.Manager()
    this_hangs = manager.Value("i", 10)  # presence of this resource hangs the process

    worker = multiprocessing.Process(
        target=failing_function,
    )
    worker.start()

    wait_for_processes([worker])


if __name__ == "__main__":
    sentry_sdk.init(
        dsn=os.environ.get("SENTRY_DSN"),
        debug=True,
    )
    execute()
