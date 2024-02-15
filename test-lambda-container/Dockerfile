FROM public.ecr.aws/lambda/python:3.11

# Add Sentry Layer
COPY --from=public.ecr.aws/sentry/sentry-python-serverless-sdk:6 /opt/ /opt

# Copy requirements.txt
COPY requirements.txt ${LAMBDA_TASK_ROOT}

# Copy function code
COPY lambda_function.py ${LAMBDA_TASK_ROOT}

# Install the specified packages
RUN pip install -r requirements.txt

ENV SENTRY_INITIAL_HANDLER="lambda_function.handler"
ENV SENTRY_DSN="https://d655584d05f14c58b86e9034aab6817f@o447951.ingest.sentry.io/5461230"
ENV SENTRY_TRACES_SAMPLE_RATE="1.0"

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
#CMD [ "lambda_function.handler" ]

CMD ["sentry_sdk.integrations.init_serverless_sdk.sentry_lambda_handler"]

