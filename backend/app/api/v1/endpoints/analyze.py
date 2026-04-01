from fastapi import APIRouter
from app.models.migration import AnalyzeRequest, AnalyzeResponse
from app.services.analysis.prompt_analyzer import PromptAnalyzer

router = APIRouter()

@router.post("/", response_model=AnalyzeResponse)
async def analyze_workload(request: AnalyzeRequest):
    """
    Analyzes the source LLM workload and recommends a Bedrock model.
    Now connected to PromptAnalyzer (Person 2).
    """
    # PromptAnalyzer handles complex mapping and parsing using static methods
    result = PromptAnalyzer.analyze_and_translate(
        payload=request.prompt,
        source_model=request.model
    )

    # FastAPI will automatically validate and parse this dict into AnalyzeResponse
    return result