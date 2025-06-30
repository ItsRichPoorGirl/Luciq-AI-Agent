#!/usr/bin/env python3
"""
Script to manually enable feature flags for Luciq deployment.
This ensures that custom_agents, agent_marketplace, and workflows are enabled.
"""

import asyncio
import sys
import os

# Add the backend directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

async def enable_feature_flags():
    """Enable the required feature flags for Luciq deployment."""
    try:
        from flags.flags import enable_flag
        from utils.logger import logger
        
        logger.info("Manually enabling Luciq feature flags...")
        
        # Enable the required feature flags
        flags_to_enable = [
            ("custom_agents", "Enable custom agent builder and management functionality"),
            ("agent_marketplace", "Enable agent marketplace for discovering and sharing agents"),
            ("workflows", "Enable workflow automation functionality")
        ]
        
        for flag_name, description in flags_to_enable:
            success = await enable_flag(flag_name, description)
            if success:
                logger.info(f"Successfully enabled feature flag: {flag_name}")
            else:
                logger.error(f"Failed to enable feature flag: {flag_name}")
        
        logger.info("Feature flag setup completed")
        
    except Exception as e:
        logger.error(f"Error enabling feature flags: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = asyncio.run(enable_feature_flags())
    if success:
        print("✅ Feature flags enabled successfully")
        sys.exit(0)
    else:
        print("❌ Failed to enable feature flags")
        sys.exit(1) 