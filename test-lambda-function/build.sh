#!/usr/bin/env bash

set -ex

rm -rf lambda_function_package.zip
rm -rf ./python_with_sentry/package/*

pip install --target ./python_with_sentry/package -r requirements.txt

cd ./python_with_sentry/package && zip -x "**/__pycache__/*" -r ../../lambda_function_package.zip . && cd -

cd ./python_with_sentry && zip -g ../lambda_function_package.zip lambda_function.py && cd -