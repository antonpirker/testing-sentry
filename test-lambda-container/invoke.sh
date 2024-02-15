#!/usr/bin/env bash
# Invokes the lambda function and prints the result.

# Make sure we get raw text output from AWS CLI
export AWS_DEFAULT_OUTPUT="text"
export AWS_PAGER=""

# Invoke Lambda function
aws lambda invoke --function-name test_sentry_container response.json

# Output response
cat response.json