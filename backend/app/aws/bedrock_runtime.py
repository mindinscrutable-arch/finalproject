import logging
from typing import Any, Dict, List, Optional
from app.aws.boto_session import get_boto_client

logger = logging.getLogger(__name__)

def invoke_bedrock_converse(
    model_id: str,
    messages: List[Dict[str, Any]],
    system_prompts: Optional[List[Dict[str, str]]] = None,
    inference_config: Optional[Dict[str, Any]] = None,
    tool_config: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Invokes the Amazon Bedrock Converse API with the specified model and messages.
    """
    client = get_boto_client("bedrock-runtime")
    
    kwargs = {
        "modelId": model_id,
        "messages": messages,
    }
    
    if system_prompts:
        kwargs["system"] = system_prompts
        
    if inference_config:
        kwargs["inferenceConfig"] = inference_config
        
    if tool_config:
        kwargs["toolConfig"] = tool_config

    try:
        response = client.converse(**kwargs)
        return response
    except Exception as e:
        logger.error(f"Error invoking Bedrock runtime (converse) for model {model_id}: {str(e)}")
        raise e

def invoke_bedrock_converse_stream(
    model_id: str,
    messages: List[Dict[str, Any]],
    system_prompts: Optional[List[Dict[str, str]]] = None,
    inference_config: Optional[Dict[str, Any]] = None,
    tool_config: Optional[Dict[str, Any]] = None,
):
    """
    Invokes the Amazon Bedrock ConverseStream API to stream responses.
    """
    client = get_boto_client("bedrock-runtime")
    
    kwargs = {
        "modelId": model_id,
        "messages": messages,
    }
    
    if system_prompts:
        kwargs["system"] = system_prompts
        
    if inference_config:
        kwargs["inferenceConfig"] = inference_config
        
    if tool_config:
        kwargs["toolConfig"] = tool_config

    try:
        response = client.converse_stream(**kwargs)
        for event in response.get("stream", []):
            yield event
    except Exception as e:
        logger.error(f"Error invoking Bedrock runtime (converse_stream) for model {model_id}: {str(e)}")
        raise e
