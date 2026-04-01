from fastapi import APIRouter
from app.models.migration import AnalyzeRequest, CompareResponse
from app.services.analysis.prompt_analyzer import PromptAnalyzer

# MOCK: Teammate hasn't pushed orchestrator.py yet, so we mock their function locally 
# to keep the API layer running strictly without touching the services/ folder.
async def run_comparison(source_model: str, source_payload: dict, bedrock_model: str, bedrock_payload: dict):
    return {
        "status": "success",
        "similarity_score": 0.94,
        "source": {
            "output": "Mock output from source model.",
            "latency_ms": 1250,
            "cost_usd": 0.04
        },
        "bedrock": {
            "output": "Mock output from Amazon Bedrock model. Results look great.",
            "latency_ms": 680,
            "cost_usd": 0.015
        }
    }

router = APIRouter()

@router.post("/", response_model=CompareResponse)
async def compare_models(request: AnalyzeRequest):

    # Step 1: Analyze + Translate (Using static method correctly)
    analysis = PromptAnalyzer.analyze_and_translate(
        payload=request.prompt,
        source_model=request.model
    )

    # Step 2: Execute both models
    execution_result = await run_comparison(
        source_model=request.model,
        source_payload=request.prompt,
        bedrock_model=analysis["target"]["model"],
        bedrock_payload=analysis["target"]["bedrock_payload"]
    )

    # Step 3: Return combined result
    return {
        "analysis": analysis,
        "execution": execution_result
    }