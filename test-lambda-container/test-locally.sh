#!/usr/bin/env bash

# First build the image
./build.sh

# start new container
docker run -d --rm -p 9000:8080 test_sentry_container:test &

sleep 1

curl "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{"payload":"hello you! You look amazing today!"}'