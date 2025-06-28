#!/bin/bash

# Test Admin Bypass Script
# Usage: ./test-admin-bypass.sh <JWT_TOKEN>

JWT_TOKEN=$1
BACKEND_URL="https://luciq-ai-backend.fly.dev"

if [ -z "$JWT_TOKEN" ]; then
    echo "Usage: $0 <JWT_TOKEN>"
    echo ""
    echo "To get your JWT token:"
    echo "1. Log in to your Vercel frontend"
    echo "2. Open browser console and run:"
    echo "   document.cookie.split(';').find(c => c.trim().startsWith('sb-') && c.includes('auth-token'))?.split('=')[1]"
    echo "3. Copy the token and use it here"
    exit 1
fi

echo "Testing Admin Bypass with JWT token..."
echo "Backend URL: $BACKEND_URL"
echo ""

# Test 1: Health check (should work without auth)
echo "1. Testing health check..."
curl -s "$BACKEND_URL/api/health" | jq '.'
echo ""

# Test 2: Billing available models (should trigger admin bypass)
echo "2. Testing billing available models (admin bypass)..."
curl -s -H "Authorization: Bearer $JWT_TOKEN" "$BACKEND_URL/billing/available-models" | jq '.'
echo ""

# Test 3: Billing subscription (should trigger admin bypass)
echo "3. Testing billing subscription (admin bypass)..."
curl -s -H "Authorization: Bearer $JWT_TOKEN" "$BACKEND_URL/billing/subscription" | jq '.'
echo ""

# Test 4: Debug admin status
echo "4. Testing debug admin status..."
curl -s -H "Authorization: Bearer $JWT_TOKEN" "$BACKEND_URL/api/debug/admin-status" | jq '.'
echo ""

echo "Test complete! Check the responses above."
echo "If admin bypass is working, you should see subscription data instead of 401 errors." 