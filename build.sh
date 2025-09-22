#!/bin/bash
# Exit on error
set -e

echo "=== Setting up Python environment ==="
python -m pip install --upgrade pip

# Install numpy first as pandas depends on it
echo "=== Installing core dependencies ==="
pip install --no-cache-dir numpy==1.24.3

# Install other requirements
echo "=== Installing project dependencies ==="
pip install --no-cache-dir -r requirements.txt

echo "=== Build completed successfully! ==="

exit 0
