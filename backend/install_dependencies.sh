#!/bin/bash

# Create a virtual environment in the 'venv' directory
echo "Creating a virtual environment..."
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Note: Within the virtual environment, 'pip' should automatically refer to 'pip3'.
# But we'll explicitly use 'pip3' as requested.

# Update package list and upgrade existing packages
echo "Updating and upgrading existing packages..."
sudo apt-get update && sudo apt-get upgrade -y

# Ensure pip3 is installed and up to date in the virtual environment
echo "Ensuring pip3 is installed and up to date..."
pip3 install --upgrade pip

# Install Flask
echo "Installing Flask..."
pip3 install Flask

# Install Flask-CORS
echo "Installing Flask-CORS..."
pip3 install Flask-CORS

# Install requests
echo "Installing requests..."
pip3 install requests

# Install firebase_admin
echo "Installing firebase_admin..."
pip3 install firebase_admin

# Install moviepy
echo "Installing moviepy..."
pip3 install moviepy

echo "All Python dependencies have been installed successfully inside the virtual environment."

# Reminder to deactivate the virtual environment when done
echo "To deactivate the virtual environment, run 'deactivate'."