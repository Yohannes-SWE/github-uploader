#!/bin/bash

echo "Starting GitHub Uploader services..."
echo ""

# Start FastAPI backend
echo "Starting FastAPI backend on http://localhost:8000 ..."
cd server || exit 1
python3.11 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload 