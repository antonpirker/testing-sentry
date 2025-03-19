import os

from pyspark.sql import SparkSession

import sentry_sdk
from sentry_sdk.integrations.spark import SparkIntegration
from sentry_sdk.integrations.spark.spark_worker import SparkWorkerIntegration

###
# This file is the Spark Driver (I think)
###

# Import worker functions
from worker_function import successful_task, failing_task

sentry_sdk.init(
    dsn=os.environ.get("SENTRY_DSN"),
    integrations=[
        SparkIntegration(),
        SparkWorkerIntegration(),
    ],
    traces_sample_rate=1.0,
    debug=True,
)

# Create a Spark session (this runs on the driver)
spark = SparkSession.builder \
    .appName("SparkSentryTest") \
    .master("local[2]") \
    .config("spark.python.worker.reuse", "true") \
    .config("spark.python.use.daemon", "true") \
    .config("spark.python.daemon.module", "sentry_daemon") \
    .getOrCreate()

# Add the sentry_daemon.py to worker's Python path
script_dir = os.path.dirname(os.path.abspath(__file__))
sentry_daemon_path = os.path.join(script_dir, "sentry_daemon.py")
spark.sparkContext.addPyFile(sentry_daemon_path)

try:
    # Create batches of data to process
    batches = [
        range(1, 5),
        range(5, 10), 
        range(10, 15)
    ]

    for batch in batches:
        rdd = spark.sparkContext.parallelize(batch)

        print("\n=== Running successful tasks (on workers) ===")
        results = rdd.map(successful_task).collect()
        for result in results:
            print(f"Result(successful_task): {result}")

        print("\n=== Running tasks with errors (on workers) ===")
        results = rdd.map(failing_task).collect()
        for result in results:
            print(f"Result(failing_task): {result}")
    
finally:
    # Always stop the Spark session
    spark.stop()
    print("Spark session stopped")