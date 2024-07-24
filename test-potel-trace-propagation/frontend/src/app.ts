import './instrument';

import * as Sentry from '@sentry/node';
import axios from 'axios';
import express from 'express';

const app = express();
const port = 3000;

app.get('/', async function (req, res) {
  Sentry.withActiveSpan(null, async () => {
    Sentry.startSpan({ name: 'test-transaction', op: 'function' }, async () => {
      Sentry.startSpan({ name: 'test-span' }, async () => {
        const url = 'http://localhost:5000';
        try {
          const response = await axios.get(url);
          let content = {
            content: "Express (frontend)"
          }

          content["content"] += " -> " + response.data["content"];

          res.json(content)

        } catch (error) {
          if (axios.isAxiosError(error)) {
            // Handle axios-specific error
            res.status(error.response?.status || 500).send(`Error fetching data: ${error.message}`);
          } else if (error instanceof Error) {
            // Handle generic error
            res.status(500).send(`Error fetching data: ${error.message}`);
          } else {
            // Handle unknown error
            res.status(500).send('An unknown error occurred.');
          }  }

      });
    });
  });
});

app.get("/debug-sentry", function mainHandler(req, res) {
  throw new Error("My first Sentry error!");
});

app.get('/test-transaction', function (req, res) {
  Sentry.withActiveSpan(null, async () => {
    Sentry.startSpan({ name: 'test-transaction', op: 'e2e-test' }, () => {
      Sentry.startSpan({ name: 'test-span' }, () => undefined);
    });

    await Sentry.flush();

    res.send({});
  });
});

Sentry.setupExpressErrorHandler(app);

app.use(function onError(err: unknown, req: any, res: any, next: any) {
  // The error id is attached to `res.sentry` to be returned
  // and optionally displayed to the user for support.
  res.statusCode = 500;
  res.end(res.sentry + '\n');
});

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`);
});
