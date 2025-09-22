#!/bin/bash
# Exit on error
set -e

# Install system dependencies
echo "Installing system dependencies..."
sudo apt-get update
sudo apt-get install -y python3-dev libxml2-dev libxslt1-dev zlib1g-dev

# Install Python packages
echo "Installing Python packages..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Build completed successfully!"

exit 0
