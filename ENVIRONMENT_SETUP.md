# Environment Setup Summary

## Overview
This document explains the environment configuration setup for Railway deployment of Luciq AI Agent.

## Environment Modes

The application supports three environment modes as defined in `backend/utils/config.py`:

### 1. Local (`local`)
- **Purpose**: Development environment
- **Default**: Used when no `ENV_MODE` is specified
- **Configuration**: Uses local development settings

### 2. Staging (`staging`) 
- **Purpose**: Testing and preview environment
- **Railway**: Used for Railway's preview/development environment
- **Configuration**: Same Stripe settings as production (for testing)
- **Files**: `railway.toml`, `railway-worker.toml`

### 3. Production (`production`)
- **Purpose**: Live production environment  
- **Railway**: Used for Railway's production environment
- **Configuration**: Production Stripe and service settings
- **Files**: `railway-prod.toml`, `railway-worker-prod.toml`

## Configuration Files

### Staging Environment (Preview)
```
railway.toml              # Main API service config
railway-worker.toml       # Worker service config
railway.Dockerfile        # Shared Dockerfile
```

### Production Environment
```
railway-prod.toml         # Main API service config
railway-worker-prod.toml  # Worker service config  
railway.Dockerfile        # Shared Dockerfile
```

## Environment Variable Mapping

| Railway Environment | ENV_MODE | Configuration Files |
|-------------------|----------|-------------------|
| Preview/Development | `staging` | `railway.toml` + `railway-worker.toml` |
| Production | `production` | `railway-prod.toml` + `railway-worker-prod.toml` |

## Key Differences Between Environments

### Staging vs Production

| Aspect | Staging | Production |
|--------|---------|------------|
| ENV_MODE | `staging` | `production` |
| Stripe Configuration | Same as production (for testing) | Production settings |
| Logging | Debug level | Production level |
| Resource Limits | Railway free/pro limits | Railway pro limits |
| Error Handling | Verbose | Optimized |

## Deployment Commands

### Using the Script
```bash
./deploy-railway.sh
# Choose 1 for staging, 2 for production
```

### Manual Deployment

#### Staging
```bash
# API Service
railway up --service api

# Worker Service  
railway up --service worker
```

#### Production
```bash
# API Service
railway up --service api --environment production

# Worker Service
railway up --service worker --environment production
```

## Environment Variables

### Automatically Set by Railway Config
- `ENV_MODE`: Set to `staging` or `production` based on config file
- `WORKERS`: Number of Gunicorn workers (2)
- `THREADS`: Number of threads per worker (2)
- `WORKER_CONNECTIONS`: Max connections per worker (1000)

### Required Environment Variables (Set Manually)
All other environment variables must be set manually in Railway dashboard:

#### Database
- `SUPABASE_URL`
- `SUPABASE_ANON_KEY` 
- `SUPABASE_SERVICE_ROLE_KEY`

#### Redis/RabbitMQ
- `REDIS_HOST`, `REDIS_PORT`, `REDIS_PASSWORD`, `REDIS_SSL`
- `RABBITMQ_HOST`, `RABBITMQ_PORT`, `RABBITMQ_USER`, `RABBITMQ_PASSWORD`

#### LLM APIs
- `ANTHROPIC_API_KEY`
- `OPENAI_API_KEY`
- `OPENROUTER_API_KEY`
- `MODEL_TO_USE`

#### Other Services
- `TAVILY_API_KEY`
- `FIRECRAWL_API_KEY`
- `DAYTONA_API_KEY`
- `QSTASH_URL`, `QSTASH_TOKEN`
- `MCP_CREDENTIAL_ENCRYPTION_KEY`
- And many more...

## Important Notes

1. **Don't Override ENV_MODE**: The Railway config files set this automatically
2. **Two Services Required**: Both API and worker services need the same environment variables
3. **Environment Separation**: Use different API keys for staging vs production when possible
4. **Configuration Files**: Railway automatically detects the right config based on your environment

## Troubleshooting

### Environment Mode Issues
- Verify you're using the correct configuration files for your Railway environment
- Check that `ENV_MODE` is set correctly in the Railway config
- Ensure environment variables match your chosen environment

### Service Configuration Issues
- Make sure both API and worker services exist in Railway
- Verify both services use the same `railway.Dockerfile`
- Check that environment variables are set for both services

## Migration Between Environments

### From Staging to Production
1. Create production environment in Railway
2. Use `railway-prod.toml` and `railway-worker-prod.toml`
3. Set production environment variables
4. Deploy using production commands

### From Production to Staging
1. Create preview environment in Railway  
2. Use `railway.toml` and `railway-worker.toml`
3. Set staging environment variables
4. Deploy using staging commands 