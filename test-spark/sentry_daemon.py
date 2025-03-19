import os

import pyspark.daemon as original_daemon

import sentry_sdk
from sentry_sdk.integrations.spark.spark_worker import SparkWorkerIntegration


if __name__ == '__main__':
    sentry_sdk.init(
        dsn=os.environ.get("SENTRY_DSN"),
        integrations=[
            SparkWorkerIntegration(), 
        ],
        debug=True,
    )
    
    # Do not print anything here - it interferes with Spark's daemon communication
    
    # Call the original daemon manager
    original_daemon.manager()
