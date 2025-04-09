#!/bin/bash
# Script to start Jaeger in Docker

echo "Starting Jaeger with Docker..."
echo "Jaeger UI will be available at http://localhost:16686"
echo "Press Ctrl+C to stop the containers"
echo

# Create a Docker network for both containers
echo "Creating Docker network..."
docker network create otel-net 2>/dev/null || true

# Start Jaeger first
echo "Starting Jaeger container..."
docker run --rm \
  --name otel-test-jaeger \
  --network otel-net \
  -p 16686:16686 \
  -p 14250:14250 \
  -p 4317:4317 \
  -p 4318:4318 \
  -e COLLECTOR_OTLP_ENABLED=true \
  jaegertracing/all-in-one:latest
