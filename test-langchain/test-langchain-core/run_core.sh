#!/usr/bin/env zsh

# Install uv if it's not installed
if ! command -v uv &> /dev/null; then
    curl -LsSf https://astral.sh/uv/install.sh | sh
fi

# Run the langchain-core test with the specific pyproject.toml
uv run --project pyproject_core.toml python langchain_core_test.py
