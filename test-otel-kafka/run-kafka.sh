#!/bin/bash
# Script to start Kafka in KRaft mode

echo "Starting Kafka in KRaft mode with Docker..."
echo "This will run Kafka on localhost:9092"
echo "Press Ctrl+C to stop the container"
echo

# Create a Docker network
echo "Creating Docker network..."
docker network create otel-net 2>/dev/null || true

# Start Kafka with KRaft mode
echo "Starting Kafka container in KRaft mode..."
docker run --rm \
  --name otel-test-kafka \
  --network otel-net \
  -p 9092:9092 \
  -e KAFKA_CFG_NODE_ID=1 \
  -e KAFKA_CFG_PROCESS_ROLES=broker,controller \
  -e KAFKA_CFG_CONTROLLER_QUORUM_VOTERS=1@localhost:9093 \
  -e KAFKA_CFG_LISTENERS=PLAINTEXT://:9092,CONTROLLER://:9093 \
  -e KAFKA_CFG_ADVERTISED_LISTENERS=PLAINTEXT://localhost:9092 \
  -e KAFKA_CFG_LISTENER_SECURITY_PROTOCOL_MAP=CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT \
  -e KAFKA_CFG_CONTROLLER_LISTENER_NAMES=CONTROLLER \
  -e KAFKA_CFG_OFFSETS_TOPIC_REPLICATION_FACTOR=1 \
  -e KAFKA_CFG_TRANSACTION_STATE_LOG_REPLICATION_FACTOR=1 \
  -e KAFKA_CFG_TRANSACTION_STATE_LOG_MIN_ISR=1 \
  -e KAFKA_KRAFT_CLUSTER_ID=MkU3OEVBNTcwNTJENDM2Qk \
  -e ALLOW_PLAINTEXT_LISTENER=yes \
  bitnami/kafka:latest
