#!/bin/bash
# Script to start Kafka in Docker container

echo "Starting Kafka with Docker..."
echo "This will run Kafka on localhost:9092"
echo "Press Ctrl+C to stop the container"
echo

# Using Confluent's Kafka image with ZooKeeper

# Create a Docker network for both containers
echo "Creating Docker network..."
docker network create otel-net 2>/dev/null || true

# Start ZooKeeper first
echo "Starting ZooKeeper container..."
docker run -d --rm \
  --name otel-test-zookeeper \
  --network otel-net \
  -p 2181:2181 \
  -e ZOOKEEPER_CLIENT_PORT=2181 \
  confluentinc/cp-zookeeper:latest

# Give ZooKeeper a moment to start
echo "Waiting for ZooKeeper to start..."
sleep 5

# Then start Kafka, connecting to ZooKeeper
echo "Starting Kafka container..."
docker run --rm \
  --name otel-test-kafka \
  --network otel-net \
  -p 9092:9092 \
  -e KAFKA_ZOOKEEPER_CONNECT=otel-test-zookeeper:2181 \
  -e KAFKA_LISTENERS=PLAINTEXT://0.0.0.0:9092 \
  -e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://localhost:9092 \
  -e KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1 \
  confluentinc/cp-kafka:latest

# Cleanup when the Kafka container ends
echo "Cleaning up containers..."
docker stop otel-test-zookeeper || true
