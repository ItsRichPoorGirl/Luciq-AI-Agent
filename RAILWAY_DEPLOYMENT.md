# Railway Deployment Guide

## Overview
This guide helps you deploy the Luciq AI Agent to Railway with proper configuration and troubleshooting.

## Key Differences from Upstream

**Important**: Upstream does NOT use Railway for deployment. They use:
- GitHub Actions for building Docker images
- GitHub Container Registry for image storage  
- SSH deployment to their own servers
- Docker Compose for orchestration

This Railway deployment is a **Luciq-specific adaptation** that doesn't interfere with upstream's deployment strategy.

## Prerequisites
1. Railway account
2. All required API keys and environment variables
3. Railway CLI (optional but recommended)

## Environment Modes

The application supports three environment modes:

- **`local`**: Development environment (default)
- **`staging`**: Testing/preview environment  
- **`production`**: Live production environment

### Railway Environment Mapping

| Railway Environment | Use Configuration | ENV_MODE |
|-------------------|------------------|----------|
| Preview/Development | `railway.toml` + `railway-worker.toml` | `staging` |
| Production | `railway-prod.toml` + `railway-worker-prod.toml` | `production` |

## Quick Setup

### 1. Create Railway Project
```bash
# Using Railway CLI
railway login
railway init
railway link

# Or create via Railway dashboard
```

### 2. Configure Services
Railway will automatically detect the configuration files based on your environment.

**Important**: You need to create TWO services in Railway:
1. **Main API Service**: Uses `railway.toml` (staging) or `railway-prod.toml` (production)
2. **Worker Service**: Uses `railway-worker.toml` (staging) or `railway-worker-prod.toml` (production)

### 3. Set Environment Variables
Add these environment variables in Railway dashboard for BOTH services:

#### Required Environment Variables
```bash
# Environment Mode (automatically set by Railway config)
# ENV_MODE=staging  # for preview environment
# ENV_MODE=production  # for production environment

# Database (Supabase)
SUPABASE_URL=your-supabase-url
SUPABASE_ANON_KEY=your-supabase-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-supabase-service-role-key

# Redis Configuration (Use Railway's Redis plugin or external service)
REDIS_HOST=your-redis-host
REDIS_PORT=6379
REDIS_PASSWORD=your-redis-password
REDIS_SSL=true

# RabbitMQ Configuration (Use Railway's RabbitMQ plugin or external service)
RABBITMQ_HOST=your-rabbitmq-host
RABBITMQ_PORT=5672
RABBITMQ_USER=your-rabbitmq-user
RABBITMQ_PASSWORD=your-rabbitmq-password

# LLM Providers (at least one required)
ANTHROPIC_API_KEY=your-anthropic-key
OPENAI_API_KEY=your-openai-key
OPENROUTER_API_KEY=your-openrouter-key
MODEL_TO_USE=anthropic/claude-sonnet-4-20250514

# Search and Web Scraping
TAVILY_API_KEY=your-tavily-key
FIRECRAWL_API_KEY=your-firecrawl-key
FIRECRAWL_URL=https://api.firecrawl.dev

# Agent Execution
DAYTONA_API_KEY=your-daytona-key
DAYTONA_SERVER_URL=https://app.daytona.io/api
DAYTONA_TARGET=us

# Background Job Processing (Required)
QSTASH_URL=https://qstash.upstash.io
QSTASH_TOKEN=your-qstash-token
QSTASH_CURRENT_SIGNING_KEY=your-current-signing-key
QSTASH_NEXT_SIGNING_KEY=your-next-signing-key
WEBHOOK_BASE_URL=https://your-railway-domain.railway.app

# MCP Configuration
MCP_CREDENTIAL_ENCRYPTION_KEY=your-generated-encryption-key

# Optional APIs
RAPID_API_KEY=your-rapidapi-key
SMITHERY_API_KEY=your-smithery-key

# Frontend URL
NEXT_PUBLIC_URL=https://your-frontend-domain.railway.app
```

### 4. Deploy
```bash
railway up
```

## Architecture Differences

### Upstream Architecture
```
GitHub Actions → GitHub Container Registry → SSH → Docker Compose → Production Servers
```

### Railway Architecture  
```
Railway Build → Railway Container Registry → Railway Runtime → Railway Infrastructure
```

## Multiple Services Setup

### Service 1: Main API
- **Staging**: `railway.toml` + `railway.Dockerfile`
- **Production**: `railway-prod.toml` + `railway.Dockerfile`
- **Command**: Gunicorn web server
- **Port**: `$PORT` (Railway assigned)

### Service 2: Worker
- **Staging**: `railway-worker.toml` + `railway.Dockerfile`
- **Production**: `railway-worker-prod.toml` + `railway.Dockerfile`
- **Command**: Dramatiq worker
- **Port**: Not exposed (background processing)

## Environment-Specific Configuration

### Staging Environment (Preview)
- Uses `staging` environment mode
- Same Stripe configuration as production (for testing)
- Reduced resource limits
- Debug logging enabled

### Production Environment
- Uses `production` environment mode
- Production Stripe configuration
- Optimized resource allocation
- Production logging levels

## Troubleshooting Common Issues

### 1. Build Failures
**Problem**: Docker build fails
**Solutions**:
- Check that all files are committed to git
- Verify `railway.Dockerfile` exists and is correct
- Ensure `backend/pyproject.toml` and `backend/uv.lock` exist
- Railway doesn't support Docker BuildKit cache mounts (hence the separate Dockerfile)

### 2. Memory/CPU Limits
**Problem**: Service crashes due to resource limits
**Solutions**:
- Railway has lower resource limits than upstream's production setup
- The `railway.Dockerfile` uses reduced worker counts (2 workers vs 33)
- Monitor Railway dashboard for resource usage
- Consider upgrading Railway plan if needed

### 3. Environment Variables
**Problem**: Application fails due to missing environment variables
**Solutions**:
- Verify all required environment variables are set in Railway
- Check variable names match exactly (case-sensitive)
- Use Railway's environment variable validation
- **Important**: Set environment variables for BOTH services
- **Important**: Don't override `ENV_MODE` - it's set by the Railway config

### 4. Port Configuration
**Problem**: Service not accessible
**Solutions**:
- Railway automatically provides `$PORT` environment variable
- The `railway.Dockerfile` uses `$PORT` for binding
- Check Railway dashboard for assigned port

### 5. Health Check Failures
**Problem**: Railway reports unhealthy service
**Solutions**:
- Verify `/api/health` endpoint exists and responds
- Check application logs in Railway dashboard
- Ensure all dependencies (Redis, RabbitMQ) are running

### 6. Database Connection Issues
**Problem**: Cannot connect to Supabase
**Solutions**:
- Verify Supabase URL and keys are correct
- Check Supabase project is active
- Ensure IP allowlist includes Railway's IPs

### 7. Redis/RabbitMQ Connection Issues
**Problem**: Cannot connect to Redis or RabbitMQ
**Solutions**:
- Use Railway's Redis and RabbitMQ plugins
- Or use external services (Upstash Redis, CloudAMQP)
- Ensure connection strings are correct
- Check SSL settings match your provider

### 8. Worker Service Issues
**Problem**: Worker service fails to start or can't find modules
**Solutions**:
- Ensure both services use the same `railway.Dockerfile`
- Verify `dramatiq` is in `pyproject.toml` dependencies
- Check that environment variables are set for both services
- Monitor worker logs separately from API logs

### 9. Environment Mode Issues
**Problem**: Application behaves differently than expected
**Solutions**:
- Verify `ENV_MODE` is set correctly in Railway config
- Check that you're using the right configuration files for your environment
- Ensure Stripe and other service configurations match your environment

## Monitoring and Logs

### View Logs
```bash
# API service logs
railway logs --service api

# Worker service logs  
railway logs --service worker

# All logs
railway logs
```

### Monitor Resources
- Use Railway dashboard to monitor CPU, memory, and disk usage
- Set up alerts for resource thresholds

## Scaling Considerations

### Current Limits (Railway Free/Pro)
- Memory: 512MB-8GB per service
- CPU: 0.5-4 vCPUs per service
- Storage: 1GB-100GB

### Recommended Upgrades
- Upgrade to Pro plan for higher resource limits
- Consider separate services for different components
- Use external Redis/RabbitMQ services for better performance

## Security Best Practices

1. **Environment Variables**: Never commit sensitive data to git
2. **API Keys**: Rotate keys regularly
3. **Access Control**: Use Railway's access controls
4. **Monitoring**: Set up alerts for unusual activity
5. **Environment Separation**: Use different API keys for staging vs production

## Support

If you continue to experience issues:
1. Check Railway's status page
2. Review application logs thoroughly
3. Verify all environment variables are set correctly
4. Consider using Railway's support channels

## Notes on Upstream Compatibility

- The `railway.Dockerfile` is separate from `backend/Dockerfile` to avoid conflicts
- Railway-specific changes don't affect upstream's deployment strategy
- When syncing with upstream, only merge changes that don't affect Railway deployment
- Keep Railway configuration files in `.gitignore` if they contain sensitive data 