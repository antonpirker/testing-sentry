#!/usr/bin/env bash

set -euo pipefail

reset

# Set up environment variables for API keys
# export OPENAI_API_KEY="your-openai-key-here"
# export ANTHROPIC_API_KEY="your-anthropic-key-here"
# export SENTRY_DSN="your-sentry-dsn-here"

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

python3 main_tool.py