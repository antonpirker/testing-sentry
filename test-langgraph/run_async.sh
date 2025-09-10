#!/bin/bash

# Load environment variables
if [ -f .env ]; then
    source .env
    echo "Loaded .env file"
else
    echo "Warning: .env file not found"
fi

# Run the async multi-agent example
echo "Running async multi-agent LangGraph example..."
uv run python multi_agent_async.py
