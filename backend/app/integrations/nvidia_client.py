import logging
import time
import requests
from typing import List, Dict, Any
from app.core.config import settings

logger = logging.getLogger(__name__)

def call_nvidia(messages: List[Dict[str, Any]], target_model: str = "meta/llama3-70b-instruct") -> Dict[str, Any]:
    """
    Synchronous HTTP client triggering the NVIDIA NIMs REST endpoint dynamically over multi-family catalogs.
    Built with graceful exception handling to return a fallback string
    when the API key is invalid or networking fails.
    """
    url = "https://integrate.api.nvidia.com/v1/chat/completions"
    api_key = getattr(settings, "NVIDIA_API_KEY", "dummy_key")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": target_model,
        "messages": messages
    }
    
    try:
        # Check for meta llama to use Groq fallback for stability
        if "llama-3.1-8b" in target_model.lower():
            from app.integrations.groq_client import invoke_source_model
            import asyncio
            import json
            
            payload_str = json.dumps(messages)
            compatible_model = "llama-3.1-8b-instant"
            
            # call_nvidia is run in a separate thread, so we can use asyncio.run safely
            result = asyncio.run(invoke_source_model(compatible_model, payload_str))
            
            if result.get("latency_ms", 0) > 0:
                return {
                    "content": result.get("text", "Groq fallback successful"),
                    "latency_ms": result.get("latency_ms", 0),
                    "tokens": result.get("tokens", 1),
                    "success": True
                }
            
        start_time = time.time()
        response = requests.post(url, headers=headers, json=payload, timeout=20)
        end_time = time.time()
        response.raise_for_status()
        
        data = response.json()
        content = data["choices"][0]["message"]["content"]
        
        # Safely extract token usage or estimate
        tokens = data.get("usage", {}).get("total_tokens")
        if tokens is None:
            tokens = len(content.split())
            
        return {
            "content": content,
            "latency_ms": int((end_time - start_time) * 1000),
            "tokens": tokens,
            "success": True
        }
        
    except Exception as e:
        logger.error(f"NVIDIA API failed: {e}")
        return {
            "content": f"NVIDIA API Error: {str(e)[:50]}",
            "latency_ms": 1200,
            "tokens": 0,
            "success": False
        }
