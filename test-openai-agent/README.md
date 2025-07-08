
## Prerequisites

You need to have Python and `curl` installed.

## Configure

Set the following environment variables:
- `SENTRY_DSN`
- `OPENAI_API_KEY`

## Run

Just call this to run three agents (one doing a handoff and by calling it twice also uses cached tokens, and one doing reasoning):
```bash
./run.sh
```
