from typing import Any, Dict, List, Optional
from app.aws.bedrock_runtime import invoke_bedrock_converse, invoke_bedrock_converse_stream

class BedrockClient:
    """
    Client for interacting with Amazon Bedrock integration wrapper.
    Provides standard methods to generate chat completions and stream them.
    """
    
    def __init__(self, default_model: str = "anthropic.claude-3-sonnet-20240229-v1:0"):
        self.default_model = default_model
        
    def generate_chat_response(
        self,
        messages: List[Dict[str, Any]],
        model_id: Optional[str] = None,
        system_prompts: Optional[List[Dict[str, str]]] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        stop_sequences: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Generate a single chat response from a Bedrock model.
        """
        model = model_id or self.default_model
        
        inference_config = {
            "temperature": temperature,
            "maxTokens": max_tokens,
        }
        if stop_sequences:
            inference_config["stopSequences"] = stop_sequences
            
        return invoke_bedrock_converse(
            model_id=model,
            messages=messages,
            system_prompts=system_prompts,
            inference_config=inference_config,
        )

    def stream_chat_response(
        self,
        messages: List[Dict[str, Any]],
        model_id: Optional[str] = None,
        system_prompts: Optional[List[Dict[str, str]]] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        stop_sequences: Optional[List[str]] = None,
    ):
        """
        Generate a streaming chat response from a Bedrock model.
        """
        model = model_id or self.default_model
        
        inference_config = {
            "temperature": temperature,
            "maxTokens": max_tokens,
        }
        if stop_sequences:
            inference_config["stopSequences"] = stop_sequences
            
        yield from invoke_bedrock_converse_stream(
            model_id=model,
            messages=messages,
            system_prompts=system_prompts,
            inference_config=inference_config,
        )
