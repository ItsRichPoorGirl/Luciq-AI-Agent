#!/usr/bin/env python3
"""
Luciq AI Agent Diagnostic Script
Tests all critical components to identify issues
"""

import os
import asyncio
import httpx
import json
from datetime import datetime

class LuciqDiagnostic:
    def __init__(self):
        self.backend_url = "https://luciq-ai-backend.fly.dev"
        self.results = []
        
    def log(self, component: str, status: str, message: str, details: dict = None):
        """Log diagnostic results"""
        result = {
            "component": component,
            "status": status,
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "details": details or {}
        }
        self.results.append(result)
        print(f"[{status.upper()}] {component}: {message}")
        
    async def test_backend_health(self):
        """Test backend health endpoint"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.backend_url}/api/health", timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    self.log("Backend Health", "PASS", "Backend is responding", data)
                else:
                    self.log("Backend Health", "FAIL", f"Backend returned {response.status_code}")
        except Exception as e:
            self.log("Backend Health", "FAIL", f"Backend connection failed: {str(e)}")
    
    async def test_smithery_api(self):
        """Test Smithery API connectivity"""
        try:
            async with httpx.AsyncClient() as client:
                # Test without API key (should return error about missing key)
                response = await client.get("https://registry.smithery.ai/servers", timeout=10)
                if "Missing API key" in response.text:
                    self.log("Smithery API", "PASS", "Smithery API is accessible (requires API key)")
                else:
                    self.log("Smithery API", "WARN", f"Unexpected response: {response.text[:100]}")
        except Exception as e:
            self.log("Smithery API", "FAIL", f"Smithery API connection failed: {str(e)}")
    
    async def test_daytona_connectivity(self):
        """Test Daytona API connectivity"""
        try:
            async with httpx.AsyncClient() as client:
                # Test Daytona API endpoint
                response = await client.get("https://app.daytona.io/api/health", timeout=10)
                if response.status_code in [200, 401, 403]:  # Any response means it's reachable
                    self.log("Daytona API", "PASS", "Daytona API is accessible")
                else:
                    self.log("Daytona API", "WARN", f"Daytona API returned {response.status_code}")
        except Exception as e:
            self.log("Daytona API", "FAIL", f"Daytona API connection failed: {str(e)}")
    
    async def test_mcp_endpoints(self):
        """Test MCP endpoints (without auth)"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.backend_url}/api/mcp/servers", timeout=10)
                if response.status_code == 401:
                    self.log("MCP Endpoints", "PASS", "MCP endpoints are working (require authentication)")
                else:
                    self.log("MCP Endpoints", "WARN", f"MCP endpoint returned {response.status_code}")
        except Exception as e:
            self.log("MCP Endpoints", "FAIL", f"MCP endpoint test failed: {str(e)}")
    
    async def test_environment_variables(self):
        """Check if critical environment variables are set in Fly.io"""
        # This would require Fly.io CLI access to check secrets
        # For now, we'll note what should be checked
        required_vars = [
            "DAYTONA_API_KEY", "DAYTONA_SERVER_URL", "DAYTONA_TARGET",
            "SMITHERY_API_KEY", "SUPABASE_URL", "SUPABASE_ANON_KEY",
            "ANTHROPIC_API_KEY", "TAVILY_API_KEY", "FIRECRAWL_API_KEY"
        ]
        self.log("Environment Variables", "INFO", f"Need to verify these variables in Fly.io: {', '.join(required_vars)}")
    
    async def test_supabase_connectivity(self):
        """Test Supabase connectivity"""
        try:
            # Test Supabase health endpoint
            async with httpx.AsyncClient() as client:
                response = await client.get("https://supabase.com/health", timeout=10)
                if response.status_code == 200:
                    self.log("Supabase", "PASS", "Supabase is accessible")
                else:
                    self.log("Supabase", "WARN", f"Supabase health check returned {response.status_code}")
        except Exception as e:
            self.log("Supabase", "FAIL", f"Supabase connection failed: {str(e)}")
    
    async def run_all_tests(self):
        """Run all diagnostic tests"""
        print("🔍 Running Luciq AI Agent Diagnostics...\n")
        
        await self.test_backend_health()
        await self.test_smithery_api()
        await self.test_daytona_connectivity()
        await self.test_mcp_endpoints()
        await self.test_supabase_connectivity()
        await self.test_environment_variables()
        
        print(f"\n📊 Diagnostic Summary:")
        print(f"Total tests: {len(self.results)}")
        
        passes = len([r for r in self.results if r['status'] == 'PASS'])
        fails = len([r for r in self.results if r['status'] == 'FAIL'])
        warns = len([r for r in self.results if r['status'] == 'WARN'])
        
        print(f"✅ Passed: {passes}")
        print(f"❌ Failed: {fails}")
        print(f"⚠️  Warnings: {warns}")
        
        if fails > 0:
            print(f"\n🚨 Critical Issues Found:")
            for result in self.results:
                if result['status'] == 'FAIL':
                    print(f"  - {result['component']}: {result['message']}")
        
        return self.results

async def main():
    diagnostic = LuciqDiagnostic()
    results = await diagnostic.run_all_tests()
    
    # Save results to file
    with open('diagnostic_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n💾 Results saved to diagnostic_results.json")

if __name__ == "__main__":
    asyncio.run(main()) 