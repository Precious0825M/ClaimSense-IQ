#!/usr/bin/env python3
"""
Debug script to test IBM watsonx.ai authentication
Run this to verify your API key and get an IAM token
"""

import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_KEY = os.getenv("GRANITE_API_KEY")
PROJECT_ID = os.getenv("GRANITE_PROJECT_ID")

print("=" * 60)
print("IBM watsonx.ai Authentication Test")
print("=" * 60)

# Step 1: Get IAM Token
print("\n1. Getting IAM token from API key...")
print(f"   API Key: {API_KEY[:10]}...{API_KEY[-10:] if len(API_KEY) > 20 else ''}")

iam_url = "https://iam.cloud.ibm.com/identity/token"
headers = {
    "Content-Type": "application/x-www-form-urlencoded"
}
data = {
    "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
    "apikey": API_KEY
}

try:
    response = requests.post(iam_url, headers=headers, data=data)
    response.raise_for_status()
    token_data = response.json()
    access_token = token_data["access_token"]
    print(f"   ✅ IAM Token obtained: {access_token[:20]}...")
    print(f"   Token expires in: {token_data.get('expires_in', 'unknown')} seconds")
except Exception as e:
    print(f"   ❌ Failed to get IAM token: {e}")
    print(f"   Response: {response.text if 'response' in locals() else 'No response'}")
    exit(1)

# Step 2: Test watsonx.ai API
print("\n2. Testing watsonx.ai API...")
print(f"   Project ID: {PROJECT_ID}")

watsonx_url = "https://us-south.ml.cloud.ibm.com/ml/v1/text/chat"
params = {
    "version": "2024-03-19",
    "project_id": PROJECT_ID
}
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}
payload = {
    "model": "ibm/granite-13b-chat-v2",
    "messages": [
        {"role": "user", "content": "Say 'Hello' if you can hear me"}
    ],
    "max_tokens": 50
}

try:
    response = requests.post(watsonx_url, headers=headers, params=params, json=payload)
    response.raise_for_status()
    result = response.json()
    print(f"   ✅ API call successful!")
    print(f"   Response: {result}")
except Exception as e:
    print(f"   ❌ API call failed: {e}")
    print(f"   Status: {response.status_code if 'response' in locals() else 'No response'}")
    print(f"   Response: {response.text if 'response' in locals() else 'No response'}")
    exit(1)

print("\n" + "=" * 60)
print("✅ All tests passed! Your configuration is correct.")
print("=" * 60)

# Made with Bob
