#!/bin/bash

# Start Mock Server Script

echo "🚀 Starting mock server..."

# Check if port is available
if lsof -Pi :5000 -sTCP:LISTEN -t >/dev/null ; then
    echo "⚠️  Port 5000 is already in use"
    echo "💡 Stopping existing process..."
    pkill -f "mock_server.py"
    sleep 2
fi

# Start mock server
python3 mock_server.py --host localhost --port 5000 &

# Wait for server to start
echo "⏳ Waiting for server to start..."
sleep 3

# Check if server is running
if curl -s "http://localhost:5000/health" > /dev/null; then
    echo "✅ Mock server is running on http://localhost:5000"
    echo "📋 Server PID: $!"
else
    echo "❌ Failed to start mock server"
    exit 1
fi

# Keep script running
wait
