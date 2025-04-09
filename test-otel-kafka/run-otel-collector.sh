#!/bin/bash
# Script to start OpenTelemetry Collector in Docker

echo "Starting OpenTelemetry Collector with Docker..."
echo "This will run the collector on ports 5317 (OTLP gRPC), 5318 (OTLP HTTP), and 8888 (metrics)"
echo "Press Ctrl+C to stop the containers"
echo

# Check if the config file exists
if [ ! -f "./otel-collector-config.yaml" ]; then
  echo "ERROR: otel-collector-config.yaml file not found!"
  echo "Please ensure the configuration file exists in the current directory."
  exit 1
fi

# Create a Docker network for both containers
echo "Creating Docker network..."
docker network create otel-net 2>/dev/null || true


# Then start the collector
echo "Starting OpenTelemetry Collector..."
echo "Using configuration from otel-collector-config.yaml"
echo "NOTE: Make sure your config includes the jaeger exporter pointing to otel-test-jaeger:14250"
docker run --rm \
  --name otel-test-collector \
  --network otel-net \
  -p 5317:4317 \
  -p 5318:4318 \
  -p 8888:8888 \
  -v "$(pwd)/otel-collector-config.yaml:/etc/otelcol/config.yaml" \
  otel/opentelemetry-collector-contrib:0.91.0
