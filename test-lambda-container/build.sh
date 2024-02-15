#!/usr/bin/env bash
# Build the docker container used by our lambda function.

docker build --platform linux/amd64 -t test_sentry_container:test .