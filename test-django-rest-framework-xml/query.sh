#!/usr/bin/env bash

# exit on first error
set -xe

curl 'http://localhost:8000/polls/handle_request' \
  -i \
  -X POST \
  -H 'content-type: application/xml' \
  --data '<?xml version="1.0" encoding="UTF-8"?><root></root>'