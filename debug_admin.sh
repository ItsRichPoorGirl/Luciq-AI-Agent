#!/bin/bash
echo "🔍 Admin Bypass Debug Script"
echo "=============================="
echo ""

echo "📋 Environment Variables:"
echo "ENV_MODE: ${ENV_MODE:-NOT_SET}"
echo "ADMIN_USER_IDS: ${ADMIN_USER_IDS:-NOT_SET}"
echo ""

echo "🌐 Testing Backend Debug Endpoint:"
echo "URL: http://localhost:8000/debug"
echo ""

if command -v curl &> /dev/null; then
    echo "Making request to debug endpoint..."
    curl -s http://localhost:8000/debug | python3 -m json.tool
else
    echo "curl not found. Please install curl or manually visit: http://localhost:8000/debug"
fi

echo ""
echo "📝 Next Steps:"
echo "1. Ensure ADMIN_USER_IDS environment variable is set with your user ID"
echo "2. Check the debug endpoint output above for your current_user_id"
echo "3. Verify your user ID matches the admin_user_ids list"
echo "4. If not matching, update ADMIN_USER_IDS environment variable"