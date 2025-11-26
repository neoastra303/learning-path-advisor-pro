#!/bin/bash
# Unix/Linux/macOS script to run Learning Path Advisor

echo "============================================================"
echo "  Learning Path Advisor - Quick Start"
echo "============================================================"
echo

if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Running setup..."
    python3 setup.py
    if [ $? -ne 0 ]; then
        echo "Setup failed. Please check the errors above."
        exit 1
    fi
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo
echo "Starting server..."
python run.py
