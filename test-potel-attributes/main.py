import os

import sentry_sdk
from sentry_sdk.consts import VERSION as SENTRY_SDK_VERSION

DIR = os.path.basename(os.path.dirname(os.path.abspath(__file__)))


def main():
    sentry_sdk.init(
        dsn=os.environ.get("SENTRY_DSN"),
        environment=f"{DIR}-{SENTRY_SDK_VERSION}",
        release=SENTRY_SDK_VERSION,
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
        debug=True,
    )

    with sentry_sdk.start_span(name="test-root-span") as root_span:
        root_span.set_data("test-root-data-string", "test-value")
        root_span.set_data("test-root-data-int", 1)
        root_span.set_data("test-root-data-float", 1.0)
        root_span.set_data("test-root-data-bool", True)
        root_span.set_data("test-root-data-list", [1, 2, 3])
        root_span.set_data("test-root-data-list2", ["one", "two", "three"])
        root_span.set_data("test-root-data-dict", {"key": "value", "key2": "value2"})
        root_span.set_data("test-root-data-none", None)
        root_span.set_data("test-root-data-dict-list", [{"key1": "value1"}, {"key2": "value2"}, {"key3": "value3"}])

        with sentry_sdk.start_span(name="test-span") as span:
            span.set_data("test-span-data-string", "test-value")
            span.set_data("test-span-data-int", 1)
            span.set_data("test-span-data-float", 1.0)
            span.set_data("test-span-data-bool", True)
            span.set_data("test-span-data-list", [1, 2, 3])
            span.set_data("test-span-data-list2", ["one", "two", "three"])
            span.set_data("test-span-data-dict", {"key": "value", "key2": "value2"})
            span.set_data("test-span-data-none", None)
            span.set_data("test-span-data-dict-list", [{"key1": "value1"}, {"key2": "value2"}, {"key3": "value3"}])

if __name__ == "__main__":
    main()
