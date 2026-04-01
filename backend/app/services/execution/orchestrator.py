import time
import asyncio
from typing import Dict, Any

from app.integrations.openai_client import OpenAIClient
from app.integrations.bedrock_client import BedrockClient

class ExecutionOrchestrator:
    """
    Orchestrates execution of the source provider model and the configured Bedrock alternative side-by-side.
    Tracks latency and maps both results to a consistent schema for the downstream evaluation engine.
    """
    
    def __init__(self):
        self.openai_client = OpenAIClient()
        self.bedrock_client = BedrockClient()

    async def run_comparison(
        self, 
        source_provider: str,
        source_model: str,
        source_messages: list,
        bedrock_model: str,
        bedrock_messages: list,
        inference_config: dict = None
    ) -> Dict[str, Any]:
        """
        Run both models concurrently and track their latency.
        """
        inference_config = inference_config or {}
        temperature = inference_config.get("temperature", 0.7)
        max_tokens = inference_config.get("max_tokens", 1000)

        # Define tasks based on provider
        source_task = None
        if source_provider.lower() == "openai":
            source_task = self._run_openai(source_model, source_messages, temperature, max_tokens)
        else:
            raise NotImplementedError(f"Source provider {source_provider} is not supported yet.")

        bedrock_task = self._run_bedrock(bedrock_model, bedrock_messages, temperature, max_tokens)

        # Execute side-by-side
        source_result, bedrock_result = await asyncio.gather(source_task, bedrock_task)

        return {
            "source": source_result,
            "bedrock": bedrock_result
        }

    async def _run_openai(self, model: str, messages: list, temperature: float, max_tokens: int) -> Dict[str, Any]:
        start_time = time.time()
        try:
            response = await self.openai_client.generate_chat_response(
                model_id=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            latency = (time.time() - start_time) * 1000 # milliseconds
            content = response["choices"][0]["message"]["content"]
            tokens = response["usage"]["total_tokens"]
            
            return {
                "success": True,
                "content": content,
                "latency_ms": round(latency, 2),
                "tokens": tokens,
                "raw_response": response
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "latency_ms": round((time.time() - start_time) * 1000, 2)
            }

    async def _run_bedrock(self, model: str, messages: list, temperature: float, max_tokens: int) -> Dict[str, Any]:
        start_time = time.time()
        try:
            # The Converse API client is synchronous locally; using run_in_executor to avoid blocking the event loop
            loop = asyncio.get_event_loop()
            
            # Use partials or lambda to hit the BedrockClient which wraps the converse API
            response = await loop.run_in_executor(
                None, 
                lambda: self.bedrock_client.generate_chat_response(
                    model_id=model, 
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
            )
            
            latency = (time.time() - start_time) * 1000 # milliseconds # type: ignore
            
            # Extract content from converse API format
            # { "output": { "message": { "content": [{ "text": "..." }] } } }
            output_message = response.get("output", {}).get("message", {})
            content_blocks = output_message.get("content", [])
            content = "".join([block.get("text", "") for block in content_blocks if "text" in block])
            
            usage = response.get("usage", {})
            tokens = usage.get("totalTokens", 0)
            
            return {
                "success": True,
                "content": content,
                "latency_ms": round(latency, 2),
                "tokens": tokens,
                "raw_response": response
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "latency_ms": round((time.time() - start_time) * 1000, 2)
            }
