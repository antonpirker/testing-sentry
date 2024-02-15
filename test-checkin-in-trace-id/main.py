import time

import requests
import sentry_sdk
from sentry_sdk.integrations.celery import CeleryIntegration

from tasks import add_together

# "sentry-python" on Sentry.io
DSN = "https://d655584d05f14c58b86e9034aab6817f@o447951.ingest.sentry.io/5461230"

monitor_config = {
    "schedule": {
        "type": "crontab",
        "value": "* * * * *",
    },
    "timezone": "UTC",
}

def main():
    sentry_sdk.init(
        dsn=DSN,
        debug=True,
        # traces_sample_rate=1.0,
        integrations=[
            CeleryIntegration(
                propagate_traces=False,
            ),
        ],         
    )

    # with sentry_sdk.start_transaction(op="test-celery-transaction"):
    requests.get("https://www.google.com?test=1")

    check_in_id = sentry_sdk.crons.api.capture_checkin(
        monitor_slug="test-monitor",
        monitor_config=monitor_config,
        status=sentry_sdk.crons.consts.MonitorStatus.IN_PROGRESS,
    )

    time.sleep(2)

    sentry_sdk.crons.api.capture_checkin(
        monitor_slug="test-monitor",
        monitor_config=monitor_config,
        status=sentry_sdk.crons.consts.MonitorStatus.OK,
        check_in_id=check_in_id,
        duration=2,
    )

    requests.get("https://www.google.com?test=2")

    add_together.delay(1, 2)

    raise Exception("222 Ende of main in calling function")


if __name__ == "__main__":
    main()