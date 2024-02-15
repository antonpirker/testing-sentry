#!/usr/bin/env bash

# exit on first error
set -xe

curl -i --request POST -v -d '{"bla": "blub"}' -H "Content-Type: application/json" http://localhost:8000/polls/


