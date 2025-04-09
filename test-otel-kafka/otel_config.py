"""
OpenTelemetry configuration for Kafka examples
"""
import os
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.instrumentation.confluent_kafka import ConfluentKafkaInstrumentor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import SERVICE_NAME


# Check if we should use OTLP exporter (set via environment variable)
USE_OTLP = os.environ.get('USE_OTLP', 'False').lower() in ('true', '1', 'yes')
OTLP_ENDPOINT = os.environ.get('OTLP_ENDPOINT', 'http://localhost:4317')


def configure_opentelemetry(service_name="kafka-example"):
    """Configure OpenTelemetry with appropriate providers and exporters"""
    # Create a resource that identifies your service
    resource = Resource.create({SERVICE_NAME: service_name})

    # Create a TracerProvider with the resource
    tracer_provider = TracerProvider(resource=resource)

    # Add a span processor that exports to console for debugging
    tracer_provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))

    # Add OTLP exporter if enabled
    if USE_OTLP:
        print(f"OpenTelemetry: Using OTLP exporter with endpoint {OTLP_ENDPOINT}")
        otlp_exporter = OTLPSpanExporter(endpoint=OTLP_ENDPOINT)
        tracer_provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
    else:
        print("OpenTelemetry: Using console exporter only. Set USE_OTLP=true to enable OTLP export.")

    # Set the tracer provider
    trace.set_tracer_provider(tracer_provider)

    # Instrument the confluent_kafka library
    ConfluentKafkaInstrumentor().instrument()

    return trace.get_tracer(__name__)


def configure_opentelemetry_producer():
    """Configure OpenTelemetry specifically for the producer"""
    return configure_opentelemetry(service_name="kafka-producer")


def configure_opentelemetry_consumer():
    """Configure OpenTelemetry specifically for the consumer"""
    return configure_opentelemetry(service_name="kafka-consumer")
