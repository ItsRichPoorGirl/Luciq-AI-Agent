#!/bin/bash

echo "🔍 Luciq AI Agent Diagnostic Script"
echo "=================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

BACKEND_URL="https://luciq-ai-backend.fly.dev"

# Function to test endpoint
test_endpoint() {
    local name="$1"
    local url="$2"
    local expected_status="$3"
    
    echo -n "Testing $name... "
    
    response=$(curl -s -o /dev/null -w "%{http_code}" "$url" 2>/dev/null)
    
    if [ "$response" = "$expected_status" ]; then
        echo -e "${GREEN}✅ PASS${NC} (Status: $response)"
        return 0
    else
        echo -e "${RED}❌ FAIL${NC} (Expected: $expected_status, Got: $response)"
        return 1
    fi
}

# Function to test with timeout
test_with_timeout() {
    local name="$1"
    local url="$2"
    local timeout="$3"
    
    echo -n "Testing $name... "
    
    if timeout "$timeout" curl -s "$url" >/dev/null 2>&1; then
        echo -e "${GREEN}✅ PASS${NC} (Reachable)"
        return 0
    else
        echo -e "${RED}❌ FAIL${NC} (Timeout/Unreachable)"
        return 1
    fi
}

# Initialize counters
passes=0
fails=0

echo "1. Backend Health Check"
test_endpoint "Backend Health" "$BACKEND_URL/api/health" "200" && ((passes++)) || ((fails++))

echo ""
echo "2. MCP Endpoints (Authentication Required)"
test_endpoint "MCP Servers Endpoint" "$BACKEND_URL/api/mcp/servers" "401" && ((passes++)) || ((fails++))

echo ""
echo "3. External API Connectivity"
test_with_timeout "Smithery Registry" "https://registry.smithery.ai/servers" 10 && ((passes++)) || ((fails++))
test_with_timeout "Daytona API" "https://app.daytona.io/api" 10 && ((passes++)) || ((fails++))
test_with_timeout "Supabase" "https://supabase.com" 10 && ((passes++)) || ((fails++))

echo ""
echo "4. Environment Variables Check"
echo -n "Checking Fly.io secrets... "
if flyctl secrets list -a luciq-ai-backend >/dev/null 2>&1; then
    echo -e "${GREEN}✅ PASS${NC} (Can access secrets)"
    ((passes++))
else
    echo -e "${YELLOW}⚠️  WARN${NC} (Cannot access secrets - may need login)"
    ((fails++))
fi

echo ""
echo "5. Backend Logs Check"
echo -n "Checking recent backend logs... "
recent_logs=$(flyctl logs -a luciq-ai-backend -n 2>/dev/null | grep -c "health" || echo "0")
if [ "$recent_logs" -gt 0 ]; then
    echo -e "${GREEN}✅ PASS${NC} (Backend is logging activity)"
    ((passes++))
else
    echo -e "${YELLOW}⚠️  WARN${NC} (No recent logs found)"
    ((fails++))
fi

echo ""
echo "6. Agent Activity Check"
echo -n "Checking for agent activity... "
agent_logs=$(flyctl logs -a luciq-ai-backend -n 2>/dev/null | grep -i "agent\|sandbox\|mcp" | wc -l || echo "0")
if [ "$agent_logs" -gt 0 ]; then
    echo -e "${GREEN}✅ PASS${NC} (Agent activity detected)"
    ((passes++))
else
    echo -e "${YELLOW}⚠️  WARN${NC} (No agent activity in recent logs)"
    ((fails++))
fi

echo ""
echo "=================================="
echo "📊 Diagnostic Summary"
echo "=================================="
echo -e "✅ Passed: ${GREEN}$passes${NC}"
echo -e "❌ Failed: ${RED}$fails${NC}"
echo ""

if [ $fails -eq 0 ]; then
    echo -e "${GREEN}🎉 All critical components are working!${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Check if frontend is deployed on Vercel"
    echo "2. Verify frontend-backend communication"
    echo "3. Test agent creation and execution"
else
    echo -e "${RED}🚨 Issues detected that need attention${NC}"
    echo ""
    echo "Recommended actions:"
    echo "1. Check Fly.io deployment status"
    echo "2. Verify environment variables"
    echo "3. Check backend logs for specific errors"
    echo "4. Test agent functionality"
fi

echo ""
echo "For detailed troubleshooting:"
echo "- Backend logs: flyctl logs -a luciq-ai-backend"
echo "- Environment: flyctl secrets list -a luciq-ai-backend"
echo "- Status: flyctl status -a luciq-ai-backend" 