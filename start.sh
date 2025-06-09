#!/usr/bin/env bash
# Simple startup helper for the Danus API
# Activates the virtual environment if present and launches the Flask server.

# Activate venv if it exists
if [ -d "venv" ]; then
  # shellcheck disable=SC1091
  source "venv/bin/activate"
fi

# Recommended environment variables
export PYTHONPATH="$(pwd)"
export DANUS_SKIP_MODEL=${DANUS_SKIP_MODEL:-1}

python api.py
