# mysettings.py
import os
import sentry_sdk

sentry_settings = {
    "dsn": os.getenv("SENTRY_DSN", None),
    "environment": os.getenv("ENV", "local"),
    "traces_sample_rate": 1.0,
    # "send_default_pii": True,
    "debug": True,
    "integrations": [],
}
print(f"Sentry Settings: {sentry_settings}")
sentry_sdk.init(**sentry_settings)
