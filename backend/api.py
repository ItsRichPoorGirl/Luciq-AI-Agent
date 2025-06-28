from fastapi import FastAPI, Request, HTTPException, Response, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
import sentry # Keep this import here, right after fastapi imports
from contextlib import asynccontextmanager
from agentpress.thread_manager import ThreadManager
from services.supabase import DBConnection
from datetime import datetime, timezone
from dotenv import load_dotenv
from utils.config import config, EnvMode
import asyncio
from utils.logger import logger, structlog
import time
from collections import OrderedDict
from typing import Dict, Any
from utils.auth_utils import get_current_user_id_from_jwt

from pydantic import BaseModel
import uuid
# Import the agent API module
from agent import api as agent_api
from sandbox import api as sandbox_api
from services import billing as billing_api
from flags import api as feature_flags_api
from services import transcription as transcription_api
from services.mcp_custom import discover_custom_tools
import sys
from email import api as email_api
import os
import sentry_sdk
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

from workflows import api as workflows_api
from webhooks import api as webhooks_api
from scheduling import api as scheduling_api
from knowledge_base import api as knowledge_base_api
from mcp_local import api as mcp_api
from mcp_local import secure_api as secure_mcp_api


load_dotenv()

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

# Initialize managers
db = DBConnection()
instance_id = "single"

# Rate limiter state
ip_tracker = OrderedDict()
MAX_CONCURRENT_IPS = 25

sentry_dsn = os.getenv("SENTRY_DSN")
if sentry_dsn:
    sentry_sdk.init(
        dsn=sentry_dsn,
        traces_sample_rate=1.0,      # Capture 100% of performance traces in staging
        profiles_sample_rate=1.0,    # Capture 100% of profiling data in staging
        environment=os.getenv("ENV_MODE", "staging"),
    )

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Starting up FastAPI application with instance ID: {instance_id} in {config.ENV_MODE.value} mode")
    try:
        await db.initialize()
        
        agent_api.initialize(
            db,
            instance_id
        )
        
        sandbox_api.initialize(db)
        
        # Initialize Redis connection
        from services import redis
        try:
            await redis.initialize_async()
            logger.info("Redis connection initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Redis connection: {e}")
            # Continue without Redis - the application will handle Redis failures gracefully
        
        # Initialize feature flags for Luciq deployment
        try:
            from flags import flags
            logger.info("Initializing Luciq feature flags...")
            await flags.enable_flag("custom_agents", "Enable custom agent builder and management functionality")
            await flags.enable_flag("agent_marketplace", "Enable agent marketplace for discovering and sharing agents")
            await flags.enable_flag("workflows", "Enable workflow automation functionality")
            logger.info("Luciq feature flags initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize feature flags: {e}")
            # Continue without feature flags - they can be set manually later
        
        # Start background tasks
        # asyncio.create_task(agent_api.restore_running_agent_runs())
        
        yield
        
        # Clean up agent resources
        logger.info("Cleaning up agent resources")
        await agent_api.cleanup()
        
        # Clean up Redis connection
        try:
            logger.info("Closing Redis connection")
            await redis.close()
            logger.info("Redis connection closed successfully")
        except Exception as e:
            logger.error(f"Error closing Redis connection: {e}")
        
        # Clean up database connection
        logger.info("Disconnecting from database")
        await db.disconnect()
    except Exception as e:
        logger.error(f"Error during application startup: {e}")
        raise

app = FastAPI(lifespan=lifespan)

@app.middleware("http")
async def log_requests_middleware(request: Request, call_next):
    structlog.contextvars.clear_contextvars()

    request_id = str(uuid.uuid4())
    start_time = time.time()
    client_ip = request.client.host
    method = request.method
    path = request.url.path
    query_params = str(request.query_params)

    structlog.contextvars.bind_contextvars(
        request_id=request_id,
        client_ip=client_ip,
        method=method,
        path=path,
        query_params=query_params
    )

    # Log the incoming request
    logger.info(f"Request started: {method} {path} from {client_ip} | Query: {query_params}")
    
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        logger.debug(f"Request completed: {method} {path} | Status: {response.status_code} | Time: {process_time:.2f}s")
        return response
    except Exception as e:
        process_time = time.time() - start_time
        logger.error(f"Request failed: {method} {path} | Error: {str(e)} | Time: {process_time:.2f}s")
        raise

# Define allowed origins based on environment
allowed_origins = [
    "https://v0-luciq-ai.vercel.app",  # Luciq production frontend
    "https://www.luciqai.com", 
    "https://luciqai.com", 
    "http://localhost:3000"
]
allow_origin_regex = None

# Add staging-specific origins
if config.ENV_MODE == EnvMode.STAGING:
    allowed_origins.extend([
        "https://staging.luciqai.com",
        "https://v0-luciq-ai.vercel.app"  # Also allow in staging
    ])
    allow_origin_regex = r"https://.*-luciq-ai\.vercel\.app"

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_origin_regex=allow_origin_regex,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "X-Project-Id"],
)

app.include_router(agent_api.router, prefix="/api")

app.include_router(sandbox_api.router, prefix="/api")

app.include_router(billing_api.router, prefix="/api")

app.include_router(feature_flags_api.router, prefix="/api")

# Add additional router inclusions without /api prefix to handle frontend requests
app.include_router(billing_api.router, prefix="")  # This makes /billing/... work
app.include_router(feature_flags_api.router, prefix="")  # This makes /feature-flags/... work

# Add agents router without /api prefix to handle frontend requests
app.include_router(agent_api.router, prefix="")  # This makes /agents/... work

# Add workflows router without /api prefix to handle frontend requests
app.include_router(workflows_api.router, prefix="")  # This makes /workflows/... work

# Add secure MCP router without /api prefix to handle frontend requests
app.include_router(secure_mcp_api.router, prefix="")  # This makes /credentials/, /templates/, etc. work

app.include_router(mcp_api.router, prefix="/api")
app.include_router(secure_mcp_api.router, prefix="/api/secure-mcp")

app.include_router(transcription_api.router, prefix="/api")
app.include_router(email_api.router, prefix="/api")

workflows_api.initialize(db)
app.include_router(workflows_api.router, prefix="/api")

webhooks_api.initialize(db)
app.include_router(webhooks_api.router, prefix="/api")

app.include_router(scheduling_api.router)

app.include_router(knowledge_base_api.router, prefix="/api")

@app.get("/api/health")
async def health_check():
    """Health check endpoint to verify API is working."""
    logger.info("Health check endpoint called")
    return {
        "status": "ok", 
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "instance_id": instance_id
    }

@app.get("/api/debug/admin-status")
async def debug_admin_status(current_user_id: str = Depends(get_current_user_id_from_jwt)):
    """Debug endpoint to check admin bypass status."""
    try:
        admin_user_ids = config.get_admin_user_ids
        is_admin = current_user_id in admin_user_ids
        
        return {
            "current_user_id": current_user_id,
            "admin_user_ids": admin_user_ids,
            "is_admin": is_admin,
            "env_mode": config.ENV_MODE.value,
            "admin_user_ids_env": os.getenv("ADMIN_USER_IDS", "NOT_SET")
        }
    except Exception as e:
        return {
            "error": str(e),
            "current_user_id": current_user_id,
            "env_mode": config.ENV_MODE.value
        }

class CustomMCPDiscoverRequest(BaseModel):
    type: str
    config: Dict[str, Any]


@app.post("/api/mcp/discover-custom-tools")
async def discover_custom_mcp_tools(request: CustomMCPDiscoverRequest):
    try:
        return await discover_custom_tools(request.type, request.config)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error discovering custom MCP tools: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/sentry-debug")
async def trigger_error():
    division_by_zero = 1 / 0

# Apply Sentry middleware at the very end, after all middleware and routes are registered
if sentry_dsn:
    app = SentryAsgiMiddleware(app)

if __name__ == "__main__":
    import uvicorn
    
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    
    workers = 1
    
    logger.info(f"Starting server on 0.0.0.0:8000 with {workers} workers")
    uvicorn.run(
        "api:app", 
        host="0.0.0.0", 
        port=8000,
        workers=workers,
        loop="asyncio"
    )