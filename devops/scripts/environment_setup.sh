#!/bin/bash

# Ensure the script exits on any error
set -e

# Install Python packages using pip
echo "Installing Python packages..."
pip install --upgrade pip
pip install --user --requirement ./app/requirements.txt

# Install wscat globally using npm
echo "Installing wscat..."
npm install --global wscat

echo "Installation complete!"