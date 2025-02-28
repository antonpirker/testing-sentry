# Example setup for testing distributed tracing with Sentry

A simple example setup for testing distributed tracing with Sentry. Just call `./run.sh` to start the frontend and backend servers.

## Explicit sampling decision (in Backend1 start_transaction(sampled=True))
```mermaid
sequenceDiagram
  actor Frontend (localhost#colon;8000)
  actor Backend1 (localhost#colon;8001) 
  actor Backend2 (localhost#colon;8002)

  Frontend (localhost#colon;8000) ->> Backend1 (localhost#colon;8001): Baggage(sample_rate=0.9, sampled=true)
  Backend1 (localhost#colon;8001) ->> Backend1 (localhost#colon;8001): start_transaction(sampled=True)
  Backend1 (localhost#colon;8001) ->> Backend2 (localhost#colon;8002): Baggage(sample_rate=0.9, sampled=true)
```


## Using `traces_sampler` (in Backend1)

```mermaid
sequenceDiagram
  actor Frontend (localhost#colon;8000)
  actor Backend1 (localhost#colon;8001)
  actor Backend2 (localhost#colon;8002)

  Frontend (localhost#colon;8000) ->> Backend1 (localhost#colon;8001): Baggage(sample_rate=0.9, sampled=true)
  Backend1 (localhost#colon;8001) ->> Backend1 (localhost#colon;8001): traces_sampler returns 0.111 <br> traces_sample_rate=1
  Backend1 (localhost#colon;8001) ->> Backend2 (localhost#colon;8002): Baggage(sample_rate=0.9, sampled=true)
```


## Using `traces_sample_rate` (in Backend1)

```mermaid
sequenceDiagram
  actor Frontend (localhost#colon;8000)
  actor Backend1 (localhost#colon;8001)
  actor Backend2 (localhost#colon;8002)

  Frontend (localhost#colon;8000) ->> Backend1 (localhost#colon;8001): Baggage(sample_rate=0.9, sampled=true)
  Backend1 (localhost#colon;8001) ->> Backend1 (localhost#colon;8001): traces_sample_rate=1
  Backend1 (localhost#colon;8001) ->> Backend2 (localhost#colon;8002): Baggage(sample_rate=0.9, sampled=true)
```