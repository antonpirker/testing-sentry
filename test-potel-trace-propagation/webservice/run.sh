#!/usr/bin/env bash

# exit on first error
set -xe

go get -u github.com/gin-gonic/gin
go get -u github.com/getsentry/sentry-go/gin

go run main.go