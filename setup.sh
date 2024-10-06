#!/bin/bash

# Check for Python installation
if ! command -v python3 &>/dev/null; then
    echo "Python is not installed. Please install Python 3."
    exit 1
fi

# Check for pip installation
if ! command -v pip &>/dev/null; then
    echo "pip is not installed. Please install pip."
    exit 1
fi

# Create a virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate the virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r app/requirements.txt

# Create .env file if it doesn't exist
if [ ! -f "app/.env" ]; then
    echo "Creating .env file. Please add your API key."
    touch app/.env
    echo "HUGGINGFACE_API_KEY=your_actual_api_key_here" > app/.env
    echo "Please edit app/.env to add your actual API key."
else
    echo ".env file already exists."
fi

# Run the FastAPI application
echo "Starting the FastAPI application..."
uvicorn app.main:app --reload

