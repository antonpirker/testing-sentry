#!/usr/bin/env bash

# exit on first error
set -euo pipefail

# Run RabbitMQ
# Server URL: amqp://guest:guest@localhost:5672
# Management console URL: http://localhost:8080
# Username: guest
# Password: guest
docker stop some-rabbit || true
docker run --rm -d --hostname my-rabbit --name some-rabbit -p 8080:15672 -p 5672:5672 rabbitmq:3-management

docker logs -f some-rabbit