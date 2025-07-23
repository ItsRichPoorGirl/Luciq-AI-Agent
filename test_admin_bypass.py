#!/usr/bin/env python3
"""
Test script to verify admin bypass functionality
"""
import os
import sys
import asyncio
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent / 'backend'
sys.path.insert(0, str(backend_dir))

from utils.config import config
from utils.auth_utils import is_admin_user
from services.billing import can_use_model, check_billing_status, get_available_models

async def test_admin_bypass():
    print("🔍 Testing Admin Bypass Configuration...")
    print(f"Environment: {os.getenv('ENV_MODE', 'NOT_SET')}")
    print(f"ADMIN_USER_IDS env: {os.getenv('ADMIN_USER_IDS', 'NOT_SET')}")
    print(f"Config admin_user_ids: {config.get_admin_user_ids}")
    print()
    
    # Test user ID (replace with your actual admin user ID)
    test_user_id = "test_admin_user"  # Replace this with your actual user ID
    
    print(f"🧪 Testing with user ID: {test_user_id}")
    print(f"Is admin user: {is_admin_user(test_user_id)}")
    print()
    
    # Test model access
    print("🎯 Testing model access...")
    try:
        # Mock client - in real usage this would be your Supabase client
        mock_client = None
        
        can_use, message, models = await can_use_model(mock_client, test_user_id, "claude-sonnet-4")
        print(f"Can use model: {can_use}")
        print(f"Message: {message}")
        print(f"Models returned: {len(models) if isinstance(models, list) else 'Not a list'}")
        print()
        
        # Test billing status
        print("💳 Testing billing status...")
        billing_status = await check_billing_status(mock_client, test_user_id)
        print(f"Billing status: {billing_status}")
        print()
        
        # Test available models
        print("📋 Testing available models...")
        available_models = await get_available_models(mock_client, test_user_id)
        print(f"Available models count: {available_models.get('total_models', 0)}")
        print(f"Subscription tier: {available_models.get('subscription_tier')}")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🚀 Admin Bypass Test Script")
    print("=" * 50)
    
    # Instructions
    print("📝 INSTRUCTIONS:")
    print("1. Set ADMIN_USER_IDS environment variable with your user ID")
    print("2. Update test_user_id in this script to match your admin user ID")
    print("3. Run this script to test admin bypass functionality")
    print("=" * 50)
    print()
    
    asyncio.run(test_admin_bypass())