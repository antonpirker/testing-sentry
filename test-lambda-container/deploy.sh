#!/usr/bin/env bash
# Builds and deploys the Lambda function and invokes it.
# See deploying the image here: https://docs.aws.amazon.com/lambda/latest/dg/python-image.html#python-image-instructions

# First build the image
./build.sh

# Make sure we get raw text output from AWS CLI
export AWS_DEFAULT_OUTPUT="text"
export AWS_PAGER=""

# Login to ECR
aws ecr get-login-password --region eu-central-1 | docker login --username AWS --password-stdin 599817902985.dkr.ecr.eu-central-1.amazonaws.com

# Create new ECR repository (will raise error if already existing, but this is ok.)
aws ecr create-repository --repository-name test_sentry_container --image-scanning-configuration scanOnPush=true --image-tag-mutability MUTABLE

# Tag the image as latest
# The uri is `repositoryUri` from the previous command
docker tag test_sentry_container:test 599817902985.dkr.ecr.eu-central-1.amazonaws.com/test_sentry_container:latest

# Push image to ECR
docker push 599817902985.dkr.ecr.eu-central-1.amazonaws.com/test_sentry_container:latest

# Create execution role
aws iam create-role --role-name lambda-execution-for-test-sentry-container --assume-role-policy-document '{"Version": "2012-10-17","Statement": [{ "Effect": "Allow", "Principal": {"Service": "lambda.amazonaws.com"}, "Action": "sts:AssumeRole"}]}'

# Add policy to execution role (for writing logs)
aws iam attach-role-policy --role-name lambda-execution-for-test-sentry-container --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

# Create Lambda function
aws lambda create-function \
  --function-name test_sentry_container \
  --package-type Image \
  --code ImageUri=599817902985.dkr.ecr.eu-central-1.amazonaws.com/test_sentry_container:latest \
  --role arn:aws:iam::599817902985:role/lambda-execution-for-test-sentry-container

# Update function code (if already existing function was changed)
aws lambda update-function-code --function-name test_sentry_container --image-uri 599817902985.dkr.ecr.eu-central-1.amazonaws.com/test_sentry_container:latest

# It takes some time for the new lambda version to be deployed
sleep 5

./invoke.sh