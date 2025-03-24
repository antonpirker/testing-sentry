#!/usr/bin/env bash

# exit on first error
set -xe

curl 'http://localhost:8000/polls/graphql/' \
  -i \
  -X POST \
  -H 'content-type: application/json' \
  --data '{
    "query": "query HelloQuery { hello }"
  }'