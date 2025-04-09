# Kafka Hello World Example with OpenTelemetry

This is a minimal example of using Apache Kafka with the confluent-kafka Python library, instrumented with OpenTelemetry for observability. Traces are sent to Jaeger or the OpenTelemetry Collector for visualization and analysis.

## Prerequisites

1. Python 3.13+ (as specified in pyproject.toml)
2. Docker installed (for running Kafka, Jaeger, and the OpenTelemetry Collector)
3. Required Python packages are automatically installed by the scripts using uv

## Setup and Running

This example includes scripts to run all components. Follow this sequence to get everything working properly:

### 1. Start Jaeger

First, start Jaeger to collect and visualize traces:

```bash
./run-jaeger.sh
```

This starts Jaeger with its UI available at http://localhost:16686.

### 2. Start the OpenTelemetry Collector

If you want to use the OpenTelemetry Collector for additional processing:

```bash
./run-otel-collector.sh
```

This collector is configured to receive traces on port 5317 and forward them to Jaeger.

### 3. Start Kafka

Start Kafka and its required ZooKeeper instance:

```bash
./run-kafka.sh
```

This script:
1. Creates a Docker network for all components
2. Starts a ZooKeeper container
3. Starts a Kafka container connected to ZooKeeper
4. Makes Kafka available at localhost:9092
5. Automatically cleans up when you stop Kafka (Ctrl+C)

### 4. Run the Producer and Consumer

In separate terminals, run the consumer and producer:

```bash
# Terminal 1
./run-consumer.sh

# Terminal 2
./run-producer.sh
```

The producer will send 5 messages, and the consumer will receive and print them. Both will generate OpenTelemetry traces that are sent to the collector and/or Jaeger.

## OpenTelemetry Instrumentation

This example includes OpenTelemetry instrumentation for Kafka:

- The `otel_config.py` file sets up OpenTelemetry with:
  - ConsoleSpanExporter (prints traces to console)
  - OTLP exporter (enabled by default in the scripts)
  - ConfluentKafkaInstrumentor for auto-instrumentation

- Both producer and consumer are instrumented with:
  - Auto-instrumentation for Kafka operations
  - Manual spans for additional context and operations
  - Custom attributes to enrich spans

The traces will show:
- Message production spans
- Message consumption spans
- Message processing spans
- Topic subscription spans

## Files in this Example

- `producer.py`: Standalone producer that sends 5 messages with OpenTelemetry instrumentation
- `consumer.py`: Standalone consumer that listens for messages with OpenTelemetry instrumentation
- `otel_config.py`: OpenTelemetry configuration and setup
- `otel-collector-config.yaml`: Configuration for the OpenTelemetry Collector
- `run-jaeger.sh`: Script to start Jaeger in Docker
- `run-otel-collector.sh`: Script to run the OpenTelemetry Collector
- `run-kafka.sh`: Script to start Kafka and ZooKeeper in Docker
- `run-consumer.sh`: Script to run the consumer
- `run-producer.sh`: Script to run the producer


## Viewing Traces

After running the producer and consumer, you can view the generated traces in Jaeger UI:

1. Open http://localhost:16686 in your browser
2. Select either "kafka-producer" or "kafka-consumer" from the Service dropdown
3. Click "Find Traces" to see all traces from the selected service
4. Explore the trace details by clicking on a trace

## Troubleshooting

1. **Connection refused**: Make sure Kafka is running and accessible at localhost:9092

2. **Topic not found**: Kafka typically creates topics automatically, but if this doesn't happen, you may need to create the topic manually:

   ```bash
   # Create topic
   docker exec -it otel-test-kafka kafka-topics \
     --create --topic hello-world-topic \
     --bootstrap-server localhost:9092 \
     --partitions 1 \
     --replication-factor 1
   ```

3. **No messages received**: Check if the producer succeeded in sending messages. The consumer is configured to read from the beginning of the topic, so it should read any existing messages.

4. **No traces in Jaeger**:
   - Ensure Jaeger is running and has the OTLP collector enabled
   - Check that the producer and consumer are using the correct OTLP endpoint
   - Verify that the OpenTelemetry Collector is correctly forwarding traces to Jaeger (if using the collector)
