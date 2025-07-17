#!/usr/bin/env bash
set -e

# Create virtual environment if it doesn't exist
if [ ! -d "./venv" ]; then
    python3 -m venv ./venv
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
