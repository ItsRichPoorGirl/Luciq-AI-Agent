#!/usr/bin/env python3
"""
Daytona VNC Connection Test Script

This script creates a test sandbox directly and attempts to verify VNC connectivity
to isolate whether the issue is with sandbox creation, VNC service startup, or
network connectivity.
"""

import asyncio
import sys
import os
import time
from typing import Optional
from datetime import datetime

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    import requests
except ImportError:
    print("⚠️  requests module not available - will skip HTTP endpoint tests")
    requests = None

from daytona_sdk import AsyncDaytona, DaytonaConfig, CreateSandboxFromSnapshotParams, Resources, SandboxState, SessionExecuteRequest
from utils.config import config
from utils.logger import logger

class DaytonaVNCTester:
    def __init__(self):
        self.daytona_config = DaytonaConfig(
            api_key=config.DAYTONA_API_KEY,
            api_url=config.DAYTONA_SERVER_URL,
            target=config.DAYTONA_TARGET,
        )
        self.daytona = AsyncDaytona(self.daytona_config)
        self.test_password = "test123vnc"  # Simple test password
        self.sandbox = None
        self.sandbox_id = None
    
    async def create_test_sandbox(self) -> bool:
        """Create a test sandbox with VNC configuration"""
        try:
            print("🔧 Creating test sandbox with VNC configuration...")
            
            params = CreateSandboxFromSnapshotParams(
                snapshot=config.SANDBOX_SNAPSHOT_NAME,  # Using the same snapshot as production
                public=True,
                labels={'test': 'vnc-connectivity'},
                env_vars={
                    "CHROME_PERSISTENT_SESSION": "true",
                    "RESOLUTION": "1024x768x24",
                    "RESOLUTION_WIDTH": "1024", 
                    "RESOLUTION_HEIGHT": "768",
                    "VNC_PASSWORD": self.test_password,
                    "ANONYMIZED_TELEMETRY": "false",
                    "CHROME_PATH": "",
                    "CHROME_USER_DATA": "",
                    "CHROME_DEBUGGING_PORT": "9222",
                    "CHROME_DEBUGGING_HOST": "localhost",
                    "CHROME_CDP": ""
                },
                resources=Resources(
                    cpu=2,
                    memory=4,
                    disk=5,
                ),
                auto_stop_interval=15,
                auto_archive_interval=2 * 60,
            )
            
            self.sandbox = await self.daytona.create(params)
            self.sandbox_id = self.sandbox.id
            print(f"✅ Sandbox created successfully: {self.sandbox_id}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to create sandbox: {str(e)}")
            return False
    
    async def wait_for_sandbox_ready(self, timeout_seconds: int = 120) -> bool:
        """Wait for sandbox to be in running state"""
        print("⏳ Waiting for sandbox to be ready...")
        print(f"   Available SandboxState values: {[attr for attr in dir(SandboxState) if not attr.startswith('_')]}")
        start_time = time.time()
        
        while time.time() - start_time < timeout_seconds:
            try:
                sandbox = await self.daytona.get(self.sandbox_id)
                print(f"   Sandbox state: {sandbox.state}")
                
                if sandbox.state == SandboxState.STARTED:
                    print("✅ Sandbox is now started and ready")
                    self.sandbox = sandbox
                    return True
                elif hasattr(SandboxState, 'FAILED') and sandbox.state == SandboxState.FAILED:
                    print(f"❌ Sandbox failed with state: {sandbox.state}")
                    return False
                elif hasattr(SandboxState, 'ARCHIVED') and sandbox.state == SandboxState.ARCHIVED:
                    print(f"❌ Sandbox archived with state: {sandbox.state}")
                    return False
                    
                await asyncio.sleep(5)
                
            except Exception as e:
                print(f"   Error checking sandbox state: {str(e)}")
                await asyncio.sleep(5)
        
        print(f"❌ Timeout waiting for sandbox to be ready after {timeout_seconds}s")
        return False
    
    async def start_supervisord(self) -> bool:
        """Start supervisord service which manages VNC and other services"""
        try:
            print("🔧 Starting supervisord service...")
            session_id = "test-supervisord"
            
            # Create session
            await self.sandbox.process.create_session(session_id)
            print(f"   Created session: {session_id}")
            
            # Start supervisord
            await self.sandbox.process.execute_session_command(session_id, SessionExecuteRequest(
                command="exec /usr/bin/supervisord -n -c /etc/supervisor/conf.d/supervisord.conf",
                var_async=True
            ))
            print("✅ Supervisord started successfully")
            
            # Wait a bit for services to start
            await asyncio.sleep(10)
            return True
            
        except Exception as e:
            print(f"❌ Failed to start supervisord: {str(e)}")
            return False
    
    async def check_vnc_processes(self) -> bool:
        """Check if VNC-related processes are running"""
        try:
            print("🔍 Checking VNC processes...")
            session_id = "check-processes"
            
            await self.sandbox.process.create_session(session_id)
            
            # Check for VNC processes
            commands = [
                "ps aux | grep vnc",
                "ps aux | grep supervisord", 
                "netstat -tlnp | grep :6080",  # VNC web port
                "netstat -tlnp | grep :5900",  # VNC port
                "supervisorctl status"
            ]
            
            for cmd in commands:
                print(f"   Running: {cmd}")
                try:
                    result = await self.sandbox.process.execute_session_command(session_id, SessionExecuteRequest(
                        command=cmd,
                        var_async=False
                    ))
                    print(f"   Output: {result}")
                except Exception as e:
                    print(f"   Error: {str(e)}")
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to check VNC processes: {str(e)}")
            return False
    
    def test_vnc_http_endpoint(self) -> bool:
        """Test VNC HTTP endpoint connectivity"""
        if not requests:
            print("⚠️  Skipping HTTP endpoint test - requests module not available")
            return True
            
        try:
            print("🌐 Testing VNC HTTP endpoint...")
            
            # Try to construct VNC URL from sandbox ID
            vnc_url = f"https://6080-{self.sandbox_id}.proxy.daytona.work"
            
            print(f"   Testing VNC URL: {vnc_url}")
            
            try:
                response = requests.get(vnc_url, timeout=10)
                print(f"   HTTP Status: {response.status_code}")
                print(f"   Response headers: {dict(response.headers)}")
                
                if response.status_code == 200:
                    print("✅ VNC HTTP endpoint is accessible")
                    return True
                else:
                    print(f"❌ VNC HTTP endpoint returned status {response.status_code}")
                    print(f"   Response body: {response.text[:500]}")
                    return False
                    
            except requests.exceptions.RequestException as e:
                print(f"❌ Failed to connect to VNC endpoint: {str(e)}")
                return False
                
        except Exception as e:
            print(f"❌ Error testing VNC endpoint: {str(e)}")
            return False
    
    async def get_sandbox_info(self) -> dict:
        """Get detailed sandbox information"""
        try:
            print("📋 Getting sandbox information...")
            sandbox = await self.daytona.get(self.sandbox_id)
            
            info = {
                'id': sandbox.id,
                'state': sandbox.state,
                'created_at': getattr(sandbox, 'created_at', 'unknown'),
                'updated_at': getattr(sandbox, 'updated_at', 'unknown'),
            }
            
            # Try to get additional info
            if hasattr(sandbox, 'git_provider_config'):
                info['git_provider_config'] = sandbox.git_provider_config
            
            if hasattr(sandbox, 'workspace'):
                info['workspace'] = sandbox.workspace
                
            print("   Sandbox Info:")
            for key, value in info.items():
                print(f"   {key}: {value}")
            
            return info
            
        except Exception as e:
            print(f"❌ Failed to get sandbox info: {str(e)}")
            return {}
    
    async def cleanup_sandbox(self) -> bool:
        """Clean up test sandbox"""
        if self.sandbox_id:
            try:
                print(f"🗑️  Cleaning up test sandbox: {self.sandbox_id}")
                await self.daytona.delete(self.sandbox)
                print("✅ Test sandbox deleted successfully")
                return True
            except Exception as e:
                print(f"❌ Failed to delete test sandbox: {str(e)}")
                return False
        return True
    
    async def run_full_test(self, cleanup: bool = True) -> bool:
        """Run the complete VNC connectivity test"""
        print("🚀 Starting Daytona VNC Connectivity Test")
        print("=" * 50)
        
        success = True
        
        try:
            # Step 1: Create sandbox
            if not await self.create_test_sandbox():
                return False
            
            # Step 2: Wait for sandbox to be ready
            if not await self.wait_for_sandbox_ready():
                return False
            
            # Step 3: Get sandbox information
            await self.get_sandbox_info()
            
            # Step 4: Start supervisord
            if not await self.start_supervisord():
                success = False
            
            # Step 5: Check VNC processes
            if not await self.check_vnc_processes():
                success = False
            
            # Step 6: Test VNC HTTP endpoint
            if not self.test_vnc_http_endpoint():
                success = False
            
            return success
            
        except Exception as e:
            print(f"❌ Test failed with exception: {str(e)}")
            return False
            
        finally:
            if cleanup:
                await self.cleanup_sandbox()

async def main():
    """Main test function"""
    print(f"Daytona VNC Test - {datetime.now()}")
    print("Testing VNC connectivity with Daytona sandboxes")
    print()
    
    # Check environment variables
    required_vars = ['DAYTONA_API_KEY', 'DAYTONA_SERVER_URL', 'DAYTONA_TARGET']
    missing_vars = [var for var in required_vars if not getattr(config, var, None)]
    
    if missing_vars:
        print(f"❌ Missing required environment variables: {missing_vars}")
        return False
    
    print("✅ All required environment variables are set")
    print(f"   DAYTONA_SERVER_URL: {config.DAYTONA_SERVER_URL}")
    print(f"   DAYTONA_TARGET: {config.DAYTONA_TARGET}")
    print()
    
    # Run the test
    tester = DaytonaVNCTester()
    
    try:
        success = await tester.run_full_test(cleanup=True)
        
        print()
        print("=" * 50)
        if success:
            print("✅ VNC connectivity test PASSED")
        else:
            print("❌ VNC connectivity test FAILED")
        
        return success
        
    except KeyboardInterrupt:
        print("\n⚠️  Test interrupted by user")
        await tester.cleanup_sandbox()
        return False
    except Exception as e:
        print(f"\n❌ Test failed with unexpected error: {str(e)}")
        await tester.cleanup_sandbox()
        return False

if __name__ == "__main__":
    # Run the test
    result = asyncio.run(main())
    sys.exit(0 if result else 1)