import os
import sentry_sdk 


def generator():
    with sentry_sdk.start_span(op="function", name="generator"):
        for x in range(10):
            with sentry_sdk.start_span(op="function", name="generator-chunk"):  # those spans work here, but not if in a Django streaming response
                yield x


def main():
    sentry_sdk.init(
        dsn=os.environ.get("SENTRY_DSN"),
        traces_sample_rate=1.0,
        debug=True,
    )

    with sentry_sdk.start_transaction(op="function", name="main"):
        print(list(generator()))


if __name__ == '__main__':
    main()