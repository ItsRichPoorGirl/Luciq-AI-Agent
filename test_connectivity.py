#!/usr/bin/env python3
"""
Connectivity Test Script for Luciq AI Agent
Tests all external service connections
"""

import asyncio
import httpx
import redis
import pika
import os
from datetime import datetime

async def test_redis_connection():
    """Test Redis connection"""
    try:
        # Get Redis config from environment
        redis_host = os.getenv('REDIS_HOST', 'lucky-sunbird-32509.upstash.io')
        redis_port = int(os.getenv('REDIS_PORT', '6379'))
        redis_password = os.getenv('REDIS_PASSWORD', '')
        redis_ssl = os.getenv('REDIS_SSL', 'true').lower() == 'true'
        
        print(f"Testing Redis connection to {redis_host}:{redis_port}")
        
        # Create Redis connection
        r = redis.Redis(
            host=redis_host,
            port=redis_port,
            password=redis_password,
            ssl=redis_ssl,
            decode_responses=True,
            socket_connect_timeout=10,
            socket_timeout=10
        )
        
        # Test connection
        result = r.ping()
        if result:
            print("✅ Redis connection successful")
            return True
        else:
            print("❌ Redis ping failed")
            return False
            
    except Exception as e:
        print(f"❌ Redis connection failed: {str(e)}")
        return False

async def test_rabbitmq_connection():
    """Test RabbitMQ connection"""
    try:
        # Get RabbitMQ config from environment
        rabbitmq_host = os.getenv('RABBITMQ_HOST', 'luciq-rabbitmq.fly.dev')
        rabbitmq_port = int(os.getenv('RABBITMQ_PORT', '5672'))
        
        print(f"Testing RabbitMQ connection to {rabbitmq_host}:{rabbitmq_port}")
        
        # Create connection parameters
        credentials = pika.PlainCredentials('guest', 'guest')
        parameters = pika.ConnectionParameters(
            host=rabbitmq_host,
            port=rabbitmq_port,
            credentials=credentials,
            socket_timeout=10,
            connection_attempts=3
        )
        
        # Test connection
        connection = pika.BlockingConnection(parameters)
        if connection.is_open:
            print("✅ RabbitMQ connection successful")
            connection.close()
            return True
        else:
            print("❌ RabbitMQ connection failed")
            return False
            
    except Exception as e:
        print(f"❌ RabbitMQ connection failed: {str(e)}")
        return False

async def test_smithery_api():
    """Test Smithery API connectivity"""
    try:
        print("Testing Smithery API connectivity")
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get("https://registry.smithery.ai/servers")
            
            if response.status_code in [200, 401]:  # 401 means API key required, which is expected
                print("✅ Smithery API accessible")
                return True
            else:
                print(f"❌ Smithery API returned {response.status_code}")
                return False
                
    except Exception as e:
        print(f"❌ Smithery API connection failed: {str(e)}")
        return False

async def test_daytona_api():
    """Test Daytona API connectivity"""
    try:
        print("Testing Daytona API connectivity")
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get("https://app.daytona.io/api")
            
            if response.status_code in [200, 401, 403]:  # Any response means it's reachable
                print("✅ Daytona API accessible")
                return True
            else:
                print(f"❌ Daytona API returned {response.status_code}")
                return False
                
    except Exception as e:
        print(f"❌ Daytona API connection failed: {str(e)}")
        return False

async def test_supabase_connection():
    """Test Supabase connectivity"""
    try:
        print("Testing Supabase connectivity")
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get("https://supabase.com")
            
            if response.status_code == 200:
                print("✅ Supabase accessible")
                return True
            else:
                print(f"❌ Supabase returned {response.status_code}")
                return False
                
    except Exception as e:
        print(f"❌ Supabase connection failed: {str(e)}")
        return False

async def main():
    """Run all connectivity tests"""
    print("🔍 Luciq AI Agent Connectivity Test")
    print("=" * 40)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print()
    
    tests = [
        ("Redis", test_redis_connection),
        ("RabbitMQ", test_rabbitmq_connection),
        ("Smithery API", test_smithery_api),
        ("Daytona API", test_daytona_api),
        ("Supabase", test_supabase_connection),
    ]
    
    results = []
    
    for name, test_func in tests:
        print(f"\n{name}:")
        try:
            result = await test_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ {name} test failed with exception: {str(e)}")
            results.append((name, False))
    
    print("\n" + "=" * 40)
    print("📊 Test Results Summary")
    print("=" * 40)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{name}: {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All connectivity tests passed!")
        print("\nNext steps:")
        print("1. Test agent creation and execution")
        print("2. Verify frontend-backend communication")
        print("3. Check MCP server integration")
    else:
        print("🚨 Some connectivity tests failed!")
        print("\nRecommended actions:")
        print("1. Check environment variables")
        print("2. Verify service credentials")
        print("3. Check network connectivity")

if __name__ == "__main__":
    asyncio.run(main()) 