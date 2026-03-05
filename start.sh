#!/usr/bin/env bash
# Danus API startup script (cross-platform)

# Detect platform and activate venv
if [ -d "venv" ]; then
  if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    # Git Bash / MinGW / Windows
    source "venv/Scripts/activate"
  else
    # macOS/Linux
    source "venv/bin/activate"
  fi
else
  echo "⚠️  No venv/ directory found — continuing without virtual environment."
fi

# Environment variables
export PYTHONPATH="$(pwd)"
export DANUS_SKIP_MODEL="${DANUS_SKIP_MODEL:-1}"

# Launch API
python api.py
