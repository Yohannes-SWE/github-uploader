#!/bin/bash

# Test Execution Script
# Usage: ./run_tests.sh [options]

set -e

# Default values
BASE_URL="http://localhost:5000"
TEST_TYPE="quick"
VERBOSE=""
COVERAGE=""
REPORT=""

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --base-url)
            BASE_URL="$2"
            shift 2
            ;;
        --full)
            TEST_TYPE="full"
            shift
            ;;
        --verbose)
            VERBOSE="--verbose"
            shift
            ;;
        --coverage)
            COVERAGE="--coverage"
            shift
            ;;
        --report)
            REPORT="--report"
            shift
            ;;
        --help)
            echo "Usage: $0 [options]"
            echo "Options:"
            echo "  --base-url URL     Base URL for testing (default: http://localhost:5000)"
            echo "  --full             Run full test suite"
            echo "  --verbose          Verbose output"
            echo "  --coverage         Run with coverage"
            echo "  --report           Generate HTML report"
            echo "  --help             Show this help"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

echo "🚀 Starting tests..."
echo "📍 Base URL: $BASE_URL"
echo "📋 Test Type: $TEST_TYPE"

# Check if server is running
echo "🔍 Checking server health..."
if ! curl -s "$BASE_URL/health" > /dev/null; then
    echo "❌ Server not responding at $BASE_URL"
    echo "💡 Start the server first: python3 server/main.py"
    exit 1
fi

echo "✅ Server is healthy"

# Run tests
python3 run_tests.py --base-url "$BASE_URL" $VERBOSE $COVERAGE $REPORT

echo "✅ Tests completed"
