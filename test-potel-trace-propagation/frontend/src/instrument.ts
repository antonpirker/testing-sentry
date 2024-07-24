const opentelemetry = require('@opentelemetry/sdk-node');
const { OTLPTraceExporter } = require('@opentelemetry/exporter-trace-otlp-http');
const Sentry = require('@sentry/node');
const { SentrySpanProcessor, SentryPropagator, SentrySampler } = require('@sentry/opentelemetry');

const sentryClient = Sentry.init({
  dsn: process.env.SENTRY_DSN,
  environment: 'qa', // dynamic sampling bias to keep transactions
  debug: true,
  includeLocalVariables: true,
  tunnel: `http://localhost:3031/`, // proxy server
  tracesSampleRate: 1,
  skipOpenTelemetrySetup: true,
});

const sdk = new opentelemetry.NodeSDK({
  sampler: sentryClient ? new SentrySampler(sentryClient) : undefined,
  textMapPropagator: new SentryPropagator(),
  contextManager: new Sentry.SentryContextManager(),
  spanProcessors: [
    new SentrySpanProcessor(),
    new opentelemetry.node.BatchSpanProcessor(
      new OTLPTraceExporter({
        url: 'http://localhost:3032/',
      }),
    ),
  ],
});

sdk.start();

Sentry.validateOpenTelemetrySetup();
