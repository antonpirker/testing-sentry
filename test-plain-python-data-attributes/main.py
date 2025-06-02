import os

import sentry_sdk


def main():
    sentry_sdk.init(
        dsn=os.environ["SENTRY_DSN"],
        # enable_tracing=True,
        traces_sample_rate=1.0,
        environment="test-plain-python-data-attributes",
        debug=True,
    )

    with sentry_sdk.start_transaction(name="xxx-test-transaction") as trx:
        with sentry_sdk.start_span(name="xxx-test-span") as span:
            # sentry_sdk.set_measurement("xxx.global.measurement.value", 1.0)

            trx.set_data("xxx.trx.data", "xxx.trx.data.value")
            # trx.set_measurement("xxx.trx.measurement.value", 1.0)
            # trx.set_attribute("xxx.trx.attribute", "xxx.trx.attribute.value")

            span.set_data("xxx.span.data", "xxx.span.data.value")
            # span.set_measurement("xxx.span.measurement.value", 1.0)
            # span.set_attribute("xxx.span.attribute", "xxx.span.attribute.value")

            division_by_zero = 1 / 0


if __name__ == "__main__":
    main()
