#!/bin/bash

# Railway Deployment Script for Luciq AI Agent
# This script helps you deploy to Railway with the correct environment configuration

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
    echo "❌ Railway CLI is not installed."
    echo "Please install it first: npm install -g @railway/cli"
    echo "Or visit: https://railway.app/cli"
    exit 1
fi

print_status "Railway CLI found"

# Check if we're in a Railway project
if ! railway status &> /dev/null; then
    echo "❌ Not in a Railway project directory."
    echo "Please run 'railway login' and 'railway init' first."
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

# Ask user for environment
echo ""
echo "Which environment do you want to deploy to?"
echo "1) Preview/Staging (uses staging config)"
echo "2) Production (uses production config)"
echo ""
read -p "Enter your choice (1 or 2): " env_choice

case $env_choice in
    1)
        echo "🎯 Deploying to Preview/Staging environment..."
        echo "Using: railway.toml + railway-worker.toml"
        echo "ENV_MODE will be set to: staging"
        
        # Check if staging configs exist
        if [ ! -f "railway.toml" ] || [ ! -f "railway-worker.toml" ]; then
            echo "❌ Staging configuration files not found!"
            echo "Please ensure railway.toml and railway-worker.toml exist."
            exit 1
        fi
        
        # Deploy to preview environment
        echo ""
        echo "📦 Deploying main API service..."
        railway up --service api
        
        echo ""
        echo "📦 Deploying worker service..."
        railway up --service worker
        
        ;;
    2)
        echo "🚀 Deploying to Production environment..."
        echo "Using: railway-prod.toml + railway-worker-prod.toml"
        echo "ENV_MODE will be set to: production"
        
        # Check if production configs exist
        if [ ! -f "railway-prod.toml" ] || [ ! -f "railway-worker-prod.toml" ]; then
            echo "❌ Production configuration files not found!"
            echo "Please ensure railway-prod.toml and railway-worker-prod.toml exist."
            exit 1
        fi
        
        # Deploy to production environment
        echo ""
        echo "📦 Deploying main API service..."
        railway up --service api --environment production
        
        echo ""
        echo "📦 Deploying worker service..."
        railway up --service worker --environment production
        
        ;;
    *)
        echo "❌ Invalid choice. Please run the script again and select 1 or 2."
        exit 1
        ;;
esac

echo ""
echo "✅ Deployment completed!"
echo ""
echo "📋 Next steps:"
echo "1. Check Railway dashboard for deployment status"
echo "2. Verify environment variables are set correctly"
echo "3. Test the health endpoint: https://your-domain.railway.app/api/health"
echo "4. Monitor logs: railway logs"
echo ""
echo "🔧 If you encounter issues:"
echo "- Check RAILWAY_DEPLOYMENT.md for troubleshooting"
echo "- Verify all required environment variables are set"
echo "- Ensure both API and worker services are running"
echo ""
echo "🌐 Your application should be available at:"
railway domain

echo ""
print_status "Railway deployment check complete!"
echo ""
print_info "Next steps:"
echo "1. Set all required environment variables in Railway dashboard"
echo "2. Monitor logs with: railway logs --tail"
echo "3. Check status with: railway status"
echo "4. View your app at the URL provided by Railway" 