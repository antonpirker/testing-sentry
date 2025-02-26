// Create and append HTML elements
document.body.innerHTML = `
  <div style="text-align: center; margin-top: 50px;">
    <h1>Sentry Tracing Test</h1>
    <button id="testButton" style="padding: 10px 20px; font-size: 16px;">
      Make Backend Request
    </button>
    <div id="result" style="margin-top: 20px;"></div>
  </div>
`;


// Initialize Sentry
// (Sentry bundle from CDN is loaded in index.html)
Sentry.init({
  dsn: "https://cdf89e7156034172a513e112d3ac10f7@o447951.ingest.us.sentry.io/4505029409374208", // "sentry-javascript" project in Sentry.io
  integrations: [
    Sentry.browserTracingIntegration({
      // Disable default pageload instrumentation
      instrumentPageLoad: false,
    }),
  ],
  tracesSampleRate: 1.0, // Capture 100% of transactions for testing
  tracePropagationTargets: ["localhost:8001", "localhost:8002"],
  debug: true,
});


// Add click handler
document.getElementById('testButton').addEventListener('click', async () => {
  const resultDiv = document.getElementById('result');

  try {
    const result = await Sentry.startSpan(
      { op: "function", name: "Making request to Backend" },
      async () => {    
        // Make the HTTP request
        const response = await fetch('http://localhost:8001/test1');
        const data = await response.json();

        resultDiv.innerHTML = `
          <h2>Response from Backend</h2>
          <pre style="
            text-align: left;
            background: #f5f5f5;
            padding: 10px;
            border-radius: 4px;
            font-family: monospace;
            white-space: pre-wrap;
            margin: 20px auto;
            max-width: 800px;
          ">${JSON.stringify(data, null, 2)}
          </pre>`;
      }
    );
  } catch (error) {
    resultDiv.textContent = `Error: ${error.message}`;
  }
});
