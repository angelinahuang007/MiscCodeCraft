#!/bin/bash

echo "Checking for Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "Python3 not found! Install it first."
    exit 1
fi

echo "Creating virtual environment..."
python3 -m venv .venv

if [ ! -d ".venv" ]; then
    echo "Virtual environment creation failed!"
    exit 1
fi

echo "Activating virtual environment..."
source .venv/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Virtual environment is set up!"
