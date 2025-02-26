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
Sentry.init({
  dsn: "https://cdf89e7156034172a513e112d3ac10f7@o447951.ingest.us.sentry.io/4505029409374208", // "sentry-javascript" project in Sentry.io
  integrations: [new Sentry.BrowserTracing()],
  tracesSampleRate: 1.0, // Capture 100% of transactions for testing
});


// Add click handler
document.getElementById('testButton').addEventListener('click', async () => {
  const resultDiv = document.getElementById('result');
  
  // Start a new transaction
  const transaction = Sentry.startTransaction({
    name: 'Backend Request',
    op: 'http.client',
  });

  // Set the transaction as current
  Sentry.getCurrentHub().configureScope(scope => {
    scope.setSpan(transaction);
  });

  try {
    // Make the HTTP request
    const response = await fetch('http://localhost:8001/test1', {
      method: 'GET',
      headers: {
        'sentry-trace': transaction.toTraceparent(),
      },
    });

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
      ">${JSON.stringify(data, null, 2)}</pre>`;
  } catch (error) {
    resultDiv.textContent = `Error: ${error.message}`;
    // Capture the error in Sentry
    Sentry.captureException(error);
  } finally {
    // Finish the transaction
    transaction.finish();
  }
});
