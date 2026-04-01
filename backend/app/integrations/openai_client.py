import os
import time
from typing import Any, Dict, List, Optional

# Expected to be installed: `pip install openai`
from openai import AsyncOpenAI

class OpenAIClient:
    """
    Client wrapper for interacting with the OpenAI API.
    """
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if self.api_key:
            self.client = AsyncOpenAI(
                api_key=self.api_key,
                base_url="https://api.x.ai/v1"
            )
        else:
            self.client = None

    async def generate_chat_response(
        self,
        messages: List[Dict[str, Any]],
        model_id: str = "grok-beta",
        temperature: float = 0.7,
        max_tokens: int = 1000,
    ) -> Dict[str, Any]:
        """
        Invokes xAI (Grok) Chat Completions API and returns the parsed response.
        Restricts the source model specifically to the list of allowed Grok models.
        """
        allowed_models = ["grok-beta", "grok-2", "grok-2-mini", "grok-2-latest"]
        if model_id not in allowed_models:
            raise ValueError(f"Unsupported source model '{model_id}'. Allowed models are: {allowed_models}")
        if not self.client:
            raise ValueError("OPENAI_API_KEY is not set.")
            
        try:
            response = await self.client.chat.completions.create(
                model=model_id,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            # Serialize the response dump so it's fully compatible with JSON
            return response.model_dump()
        except Exception as e:
            # Person A's global handler will catch this, but we log or re-raise here if needed
            raise e
