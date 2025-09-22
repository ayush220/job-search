#!/bin/bash
# Exit on error
set -e

# Install Python packages with pre-built wheels
echo "Installing Python packages..."
python -m pip install --upgrade pip
python -m pip install --no-cache-dir -r requirements.txt

echo "Build completed successfully!"

exit 0
