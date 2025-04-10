#!/bin/bash
# Script to start Jaeger in Docker

echo "Starting Jaeger with Docker..."
echo "Jaeger UI will be available at http://localhost:16686"
echo "Press Ctrl+C to stop the containers"
echo

# Create a Docker network for both containers
echo "Creating Docker network..."
docker network create otel-net 2>/dev/null || true

# Start Jaeger
echo "Starting Jaeger container..."
docker run --rm \
  --name test-otel-kafka-jaeger \
  --network otel-net \
  --label com.docker.compose.project=test-otel-kafka \
  --label com.docker.compose.service=jaeger \
  -p 16686:16686 \
  -p 4317:4317 \
  -p 4318:4318 \
  -p 5778:5778 \
  -p 9411:9411 \
  -e COLLECTOR_OTLP_ENABLED=true \
  jaegertracing/jaeger:2.5.0
