from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List

class AnalyzeRequest(BaseModel):
    provider: str = Field(..., description="Source provider (e.g., openai, vertex, azure)")
    model: str = Field(..., description="Source model name (e.g., gpt-4)")
    prompt: Dict[str, Any] = Field(..., description="JSON structure of the prompt")

class DetectedFeatures(BaseModel):
    has_system_prompt: bool
    is_json_mode: bool

class SourceInfo(BaseModel):
    provider: str
    model: str
    original_payload: Dict[str, Any]
    detected_features: DetectedFeatures

class TargetInfo(BaseModel):
    provider: str
    model: str
    mapping_reasons: List[str]
    bedrock_payload: Dict[str, Any]

class AnalyzeResponse(BaseModel):
    source: SourceInfo
    target: TargetInfo

class CompareResponse(BaseModel):
    analysis: AnalyzeResponse
    execution: Dict[str, Any]
