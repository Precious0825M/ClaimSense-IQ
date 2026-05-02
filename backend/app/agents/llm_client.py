"""LLM client wrapper for IBM Granite and Bob"""

import logging
from typing import Any, Dict, Optional
from datetime import datetime, timedelta

import httpx
from app.config import settings

logger = logging.getLogger(__name__)


class IAMTokenManager:
    """Manages IBM Cloud IAM token generation and caching"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.token = None
        self.token_expiry = None
        self.iam_url = "https://iam.cloud.ibm.com/identity/token"
    
    async def get_token(self) -> str:
        """Get valid IAM token, refreshing if needed"""
        # Check if we have a valid cached token
        if self.token and self.token_expiry and datetime.now() < self.token_expiry:
            return self.token
        
        # Get new token
        logger.info("Requesting new IAM token")
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.iam_url,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                data={
                    "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
                    "apikey": self.api_key
                }
            )
            response.raise_for_status()
            token_data = response.json()
            
            self.token = token_data["access_token"]
            # Set expiry to 5 minutes before actual expiry for safety
            expires_in = token_data.get("expires_in", 3600)
            self.token_expiry = datetime.now() + timedelta(seconds=expires_in - 300)
            
            logger.info(f"IAM token obtained, expires in {expires_in} seconds")
            return self.token


class LLMClient:
    """Base LLM client for API interactions"""
    
    def __init__(self, api_key: str, api_url: str, project_id: str = "", space_id: str = "", timeout: int = 120):
        self.api_key = api_key
        self.api_url = api_url
        self.project_id = project_id
        self.space_id = space_id
        self.timeout = timeout
        self.client = httpx.AsyncClient(timeout=timeout)
        self.token_manager = IAMTokenManager(api_key)
    
    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> str:
        """
        Generate text using LLM.
        
        Args:
            prompt: User prompt
            system_prompt: System prompt
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
        
        Returns:
            Generated text
        """
        logger.info(f"Generating LLM response (temp={temperature}, max_tokens={max_tokens})")
        
        try:
            # Prepare request payload
            payload = {
                "model": getattr(settings, "granite_model", "ibm/granite-13b-chat-v2"),
                "messages": [],
                "temperature": temperature,
                "max_tokens": max_tokens
            }
            
            # Add project_id or space_id to payload (required in body, not just URL)
            if self.project_id:
                payload["project_id"] = self.project_id
            elif self.space_id:
                payload["space_id"] = self.space_id
            
            # Add system prompt if provided
            if system_prompt:
                payload["messages"].append({
                    "role": "system",
                    "content": system_prompt
                })
            
            # Add user prompt
            payload["messages"].append({
                "role": "user",
                "content": prompt
            })
            
            # Get IAM token
            token = await self.token_manager.get_token()
            
            # Make API request
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            # Make API request
            url = f"{self.api_url}/text/chat"
            params = {"version": "2024-03-19"}
            
            logger.info(f"Sending request to: {url}")
            logger.info(f"Payload keys: {list(payload.keys())}")
            logger.info(f"Model: {payload.get('model')}")
            logger.info(f"Messages count: {len(payload.get('messages', []))}")
            
            response = await self.client.post(
                url,
                json=payload,
                headers=headers,
                params=params
            )
            
            logger.info(f"Response status: {response.status_code}")
            response.raise_for_status()
            result = response.json()
            logger.info(f"Response keys: {list(result.keys())}")
            
            # Extract generated text
            if "choices" in result and len(result["choices"]) > 0:
                generated_text = result["choices"][0]["message"]["content"]
                logger.info(f"Successfully generated {len(generated_text)} characters")
                return generated_text
            else:
                raise ValueError("No response generated from LLM")
                
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error during LLM generation: {e.response.status_code} - {e.response.text}")
            raise ValueError(f"LLM API error: {e.response.status_code}")
        except Exception as e:
            logger.error(f"Error during LLM generation: {str(e)}")
            raise
    
    async def close(self):
        """Close HTTP client"""
        await self.client.aclose()


class GraniteClient(LLMClient):
    """IBM Granite API client"""
    
    def __init__(self):
        super().__init__(
            api_key=settings.granite_api_key,
            api_url=settings.granite_api_url,
            project_id=settings.granite_project_id,
            space_id=settings.granite_space_id,
            timeout=settings.llm_timeout
        )


class BobClient(LLMClient):
    """IBM Bob API client"""
    
    def __init__(self):
        super().__init__(
            api_key=settings.bob_api_key,
            api_url=settings.bob_api_url,
            project_id=settings.bob_project_id,
            space_id=settings.bob_space_id,
            timeout=settings.llm_timeout
        )

# Made with Bob
