import sentry_sdk
from sentry_sdk.integrations.aws_lambda import AwsLambdaIntegration


sentry_sdk.init(
    dsn="https://d655584d05f14c58b86e9034aab6817f@o447951.ingest.sentry.io/5461230",
    # Add data like request headers and IP for users, if applicable;
    # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
    send_default_pii=True,
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for tracing.
    traces_sample_rate=1.0,
    # To collect profiles for all profile sessions,
    # set `profile_session_sample_rate` to 1.0.
    profile_session_sample_rate=1.0,
    # Profiles will be automatically collected while
    # there is an active span.
    profile_lifecycle="trace",
    integrations=[
        AwsLambdaIntegration(),
    ],
)


def lambda_handler(event, context):

    1/0

    return {
        'statusCode': 200,
        'body': 'Hello from Lambda!'
    }
