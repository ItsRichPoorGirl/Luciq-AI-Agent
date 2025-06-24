#!/bin/bash

# Railway Deployment Script for Luciq AI Agent
# This script helps deploy to Railway and troubleshoot issues

set -e

echo "🚂 Railway Deployment Script for Luciq AI Agent"
echo "================================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    print_error "Railway CLI not found. Install it with: npm install -g @railway/cli"
    exit 1
fi

print_status "Railway CLI found"

# Check if we're in a Railway project
if [ ! -f "railway.toml" ]; then
    print_error "railway.toml not found. Make sure you're in the project directory."
    exit 1
fi

print_status "railway.toml found"

# Check if Railway Dockerfile exists
if [ ! -f "railway.Dockerfile" ]; then
    print_error "railway.Dockerfile not found. This is required for Railway deployment."
    exit 1
fi

print_status "railway.Dockerfile found"

# Check if backend files exist
if [ ! -f "backend/pyproject.toml" ]; then
    print_error "backend/pyproject.toml not found"
    exit 1
fi

if [ ! -f "backend/uv.lock" ]; then
    print_error "backend/uv.lock not found"
    exit 1
fi

print_status "Backend files found"

# Check if we're logged into Railway
if ! railway whoami &> /dev/null; then
    print_warning "Not logged into Railway. Please run: railway login"
    railway login
fi

print_status "Logged into Railway"

# Check Railway project status
echo ""
print_info "Checking Railway project status..."
railway status

# Check Railway logs
echo ""
print_info "Recent Railway logs:"
railway logs --tail 10

# Check environment variables
echo ""
print_info "Environment variables:"
railway variables

# Ask user if they want to deploy
echo ""
read -p "Do you want to deploy to Railway? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_info "Deploying to Railway..."
    railway up
    
    echo ""
    print_status "Deployment initiated!"
    print_info "Monitor deployment with: railway logs --tail"
    print_info "Check status with: railway status"
else
    print_info "Deployment cancelled."
fi

echo ""
print_status "Railway deployment check complete!"
echo ""
print_info "Next steps:"
echo "1. Set all required environment variables in Railway dashboard"
echo "2. Monitor logs with: railway logs --tail"
echo "3. Check status with: railway status"
echo "4. View your app at the URL provided by Railway" 