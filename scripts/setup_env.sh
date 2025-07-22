#!/usr/bin/env bash
set -e

# Determine which Python interpreter to use
if command -v python3.11 >/dev/null 2>&1; then
    PYTHON_BIN="python3.11"
else
    PYTHON_BIN="python3"
fi

# Create virtual environment if it doesn't exist
if [ ! -d "./venv" ]; then
    "$PYTHON_BIN" -m venv ./venv
fi

# Activate the virtual environment
# shellcheck source=/dev/null
source ./venv/bin/activate

# Upgrade pip and install dependencies
pip install --upgrade pip
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
fi

# Message about activation
cat <<'EOM'
Virtual environment setup complete. To activate, run:
source ./venv/bin/activate
EOM
