#!/usr/bin/env bash

# exit on first error
set -xe

curl -i -v -F key1=value1 -F upload=@sample.png http://localhost:8000/polls/fileupload > output.txt
