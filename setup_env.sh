#!/usr/bin/env bash
# One-time environment setup for Danus

# Create venv if it doesn't exist
if [ ! -d "venv" ]; then
  python3 -m venv venv
fi
# Activate and install dependencies
# shellcheck disable=SC1091
source "venv/bin/activate"

pip install -r requirements.txt
