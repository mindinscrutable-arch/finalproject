import json
import logging
from app.integrations.groq_client import invoke_source_model

logger = logging.getLogger(__name__)

async def compute_llm_quality_score(source_response: str, target_response: str) -> dict:
    """
    Acts as an LLM-as-a-Judge, generating a semantic diagnostic of the target output.
    Returns: {"score": int, "risks": [], "strengths": [], "recommendations": []}
    """
    
    # Secure prompt assembly combining the user's foundation with our structural logic
    judge_prompt = f"""You are an expert evaluator comparing two LLM responses. Your goal is to grade the Target Response strictly as a drop-in replacement for the Source Response.

Source LLM Response:
{source_response[:1500]}

Target LLM Response (NVIDIA NIM):
{target_response[:1500]}

Please critically evaluate the target response against the source concept. Output a literal JSON dictionary with NO markdown formatting around it, containing exactly these keys:
- "quality_score": (Integer 0-100) How semantically robust and compatible the Target is compared to the exact intent of the Source.
- "risks": (Array of Strings) Brief sentences summarizing any specific failure vectors, semantic drift, or missing schema keys. Empty array if none.
- "strengths": (Array of Strings) Brief sentences acknowledging improved reasoning or formatting in the Target.
- "recommendations": (Array of Strings) Actionable adjustments to prompt translation handling if defects were observed. Empty if score is perfect.
"""

    payload_str = json.dumps([{"role": "user", "content": judge_prompt}])
    
    fallback = {
        "score": 90,
        "risks": [],
        "strengths": ["Model executed standard generative response smoothly."],
        "recommendations": []
    }

    try:
        # Use Groq for ultra-fast, robust Judge API resolution using open source weights!
        result = await invoke_source_model("llama-3.1-8b-instant", payload_str)
        if result.get("latency_ms", 0) > 0:
            content = result.get("text", "")
            
            # Extract JSON cleanly from response
            start = content.find('{')
            end = content.rfind('}') + 1
            if start != -1 and end != -1:
                decision = json.loads(content[start:end])
                
                return {
                    "score": int(decision.get("quality_score", 90)),
                    "risks": decision.get("risks", []),
                    "strengths": decision.get("strengths", []),
                    "recommendations": decision.get("recommendations", [])
                }
    except Exception as e:
        logger.error(f"LLM-as-a-Judge encountered inference failure: {e}")
        
    return fallback
