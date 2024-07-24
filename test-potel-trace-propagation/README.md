# test-potel-trace-propagation


This is a small setup to test trace propagation using Sentry performance powered by OTel (POtel)

It has a frontend Express JS server that makes a request to a backend Python Flask server that makes a request to a Go Gin webservice.

All parts of this distributed system have a `./run.sh` to start them. 

- `frontend` is an Express JS app using Sentry with POtel running on port `3000`.
- `backend` is a Python Flask app using Sentry with POtel running on port `5000`.
- `webservice` is a Go Gin app using Sentry **without** POtel running on port `9000`.