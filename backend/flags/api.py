from fastapi import APIRouter, Depends
from utils.logger import logger
from utils.auth_utils import get_current_user_id_from_jwt
from .flags import list_flags, is_enabled, get_flag_details, enable_flag, disable_flag

router = APIRouter()


@router.get("/feature-flags")
async def get_feature_flags():
    """Get all feature flags - public endpoint for app initialization"""
    try:
        # For public endpoint, we don't have user_id, so we use None
        # This will trigger Luciq defaults for key features
        flags = await list_flags(None)
        return {"flags": flags}
    except Exception as e:
        logger.error(f"Error fetching feature flags: {str(e)}")
        return {"flags": {}}

@router.get("/feature-flags/{flag_name}")
async def get_feature_flag(flag_name: str):
    """Get a specific feature flag - public endpoint for app initialization"""
    try:
        # For public endpoint, we don't have user_id, so we use None
        # This will trigger Luciq defaults for key features
        enabled = await is_enabled(flag_name, None)
        details = await get_flag_details(flag_name)
        return {
            "flag_name": flag_name,
            "enabled": enabled,
            "details": details
        }
    except Exception as e:
        logger.error(f"Error fetching feature flag {flag_name}: {str(e)}")
        return {
            "flag_name": flag_name,
            "enabled": False,
            "details": None
        }

@router.post("/feature-flags/{flag_name}/enable")
async def enable_feature_flag(flag_name: str):
    """Enable a feature flag"""
    try:
        success = await enable_flag(flag_name, f"Enabled via API")
        if success:
            logger.info(f"Feature flag {flag_name} enabled successfully")
            return {"success": True, "message": f"Feature flag {flag_name} enabled"}
        else:
            logger.error(f"Failed to enable feature flag {flag_name}")
            return {"success": False, "message": f"Failed to enable feature flag {flag_name}"}
    except Exception as e:
        logger.error(f"Error enabling feature flag {flag_name}: {str(e)}")
        return {"success": False, "message": str(e)}

@router.post("/feature-flags/{flag_name}/disable")
async def disable_feature_flag(flag_name: str):
    """Disable a feature flag"""
    try:
        success = await disable_flag(flag_name, f"Disabled via API")
        if success:
            logger.info(f"Feature flag {flag_name} disabled successfully")
            return {"success": True, "message": f"Feature flag {flag_name} disabled"}
        else:
            logger.error(f"Failed to disable feature flag {flag_name}")
            return {"success": False, "message": f"Failed to disable feature flag {flag_name}"}
    except Exception as e:
        logger.error(f"Error disabling feature flag {flag_name}: {str(e)}")
        return {"success": False, "message": str(e)} 