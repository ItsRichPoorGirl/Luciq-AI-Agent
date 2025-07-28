#!/bin/bash

# Daytona VNC Connectivity Test Runner
# This script runs the VNC test with proper environment setup

set -e

echo "🔧 Setting up environment for Daytona VNC test..."

# Change to backend directory
cd "$(dirname "$0")"

# Load environment variables
if [ -f .env ]; then
    echo "📁 Loading environment from .env file..."
    export $(cat .env | grep -v '^#' | xargs)
else
    echo "⚠️  No .env file found - using system environment variables"
fi

# Check if required environment variables are set
echo "🔍 Checking required environment variables..."

if [ -z "$DAYTONA_API_KEY" ]; then
    echo "❌ DAYTONA_API_KEY is not set"
    exit 1
fi

if [ -z "$DAYTONA_SERVER_URL" ]; then
    echo "❌ DAYTONA_SERVER_URL is not set"
    exit 1
fi

if [ -z "$DAYTONA_TARGET" ]; then
    echo "❌ DAYTONA_TARGET is not set"
    exit 1
fi

echo "✅ All required environment variables are set"
echo ""

# Run the test
echo "🚀 Starting Daytona VNC connectivity test..."
echo ""

if command -v uv >/dev/null 2>&1; then
    echo "Using uv to run test..."
    uv run python test_daytona_vnc.py
else
    echo "Using python to run test..."
    python test_daytona_vnc.py
fi