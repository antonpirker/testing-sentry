#!/usr/bin/env bash

# exit on first error
set -xe

# Build app
npm run build

# Run app
node dist/app.js