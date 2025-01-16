# sentry-test-server

This is a simple server that can be used to send envelopes to (instead of sending them to Sentry or a relay).
The server will print the envelopes received and the Sentry HTTP headers to the console.

## Usage

Run this one script, it will create an virtual environment and install the dependencies and then run the server on port 9999:

```
./run.sh
```

Then use `http://123@localhost:9999/0` as DSN in your SDK.
