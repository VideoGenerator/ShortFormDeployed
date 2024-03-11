#!/bin/bash

brew install jpeg
brew install libpng libtiff openjpeg

# Create a virtual environment in the 'venv' directory
echo "Creating a virtual environment..."
python3 -m venv venv

# Activate the virtual environment
echo "Activating the virtual environment..."
source venv/bin/activate

pip install Cython
pip install --upgrade setuptools wheel

echo "Installing dependencies from dependencies.txt..."
pip install -r dependencies.txt

echo "All Python dependencies have been installed successfully inside the virtual environment."

# Install boto3
echo "Installing boto3..."
pip3 install boto3


# Reminder to deactivate the virtual environment when done
echo "To deactivate the virtual environment, run 'deactivate'."


