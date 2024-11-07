#!/usr/bin/env bash

# exit on first error
set -xe

curl --header "Content-Type: application/json" \
    --request GET \
    http://localhost:8000/api/

