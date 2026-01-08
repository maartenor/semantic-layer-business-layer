#!/bin/bash
echo "Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "Starting Mock Collibra API Server..."
python app.py
