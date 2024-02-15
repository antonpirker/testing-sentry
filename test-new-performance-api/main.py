import time

import sentry_sdk


def main():
    sentry_sdk.init(
        dsn="https://d655584d05f14c58b86e9034aab6817f@o447951.ingest.sentry.io/5461230",  # sentry-python on Sentry.io
        traces_sample_rate=1.0,
        debug=True,
    )

    with sentry_sdk.start_active_span(name='outer'):
        time.sleep(0.1)
        inner1 = sentry_sdk.start_span(name='inner1')
        time.sleep(0.2)
        inner2 = sentry_sdk.start_span(name='inner2')
        time.sleep(0.3)

        with sentry_sdk.start_active_span(name='inner3'):
            time.sleep(0.4)
            inner_inner = sentry_sdk.start_span(name='innerInner')
            time.sleep(0.5)
            inner_inner.finish()
        
        inner1.finish()
        inner2.finish()

        sentry_sdk.set_measurement('outer_duration', 1500, "ms")
        

if __name__ == "__main__":
    main()