#!/usr/bin/env bash

set -ex

./build.sh

aws --profile anton_projects iam create-role --role-name lambda-ex --assume-role-policy-document '{"Version": "2012-10-17", "Statement": [{ "Effect": "Allow", "Principal": {"Service": "lambda.amazonaws.com"}, "Action": "sts:AssumeRole"}]}'

aws --profile anton_projects iam attach-role-policy --role-name lambda-ex --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

aws --profile anton_projects lambda create-function --function-name pythonWithSentry \
    --runtime python3.7 \
    --handler lambda_function.lambda_handler \
    --role arn:aws:iam::117867105546:role/lambda-ex \
    --zip-file fileb://lambda_function_package.zip