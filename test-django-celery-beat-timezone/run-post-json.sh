#!/usr/bin/env bash

# exit on first error
set -xe

curl --header "Content-Type: application/json" \
    --request POST \
    --data '{"username":"xyz","password":"xyz"}' \
    http://localhost:8000/polls/

