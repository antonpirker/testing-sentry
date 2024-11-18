import os
import sentry_sdk 


def generate():
    print(f"Inside: {sentry_sdk.get_current_scope()}")
    for x in range(10):
        yield x


def main():
    sentry_sdk.init(
        dsn=os.environ.get("SENTRY_DSN"),
        traces_sample_rate=1.0, 
        debug=True,
    )

    print(f"Before: {sentry_sdk.get_current_scope()}")
    print(list(generate()))
    print(f"After: {sentry_sdk.get_current_scope()}")


if __name__ == '__main__':
    main()