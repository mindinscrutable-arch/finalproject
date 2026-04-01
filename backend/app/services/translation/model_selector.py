import logging
from typing import Dict, Any, List
import requests
import json
from app.core.config import settings

logger = logging.getLogger(__name__)

class ModelSelector:
    """
    Intelligent AI routing engine that uses an internal LLM to evaluate NLP workloads and dynamically assign optimal NVIDIA NIM models.
    """
    
    @staticmethod
    def select_best_model(analysis: Dict[str, Any], prompt_content: str = "") -> Dict[str, str]:
        """
        Dynamically analyzes the payload and dispatches an immediate API evaluation check to map to 6 distinct models based on AI evaluation.
        """
        # Define the exact 6 models and their strengths for the LLM to choose from!
        available_models = {
            "meta/llama-3.1-405b-instruct": "Highest-tier physics, immense complexity, and dense advanced reasoning.",
            "mistralai/mixtral-8x22b-instruct-v0.1": "Flawless mathematical architecture and multi-step math calculus.",
            "qwen/qwen2.5-coder-32b-instruct": "Specialized entirely for programming, JSON parsing, code debugging and data formatting.",
            "google/gemma-2-9b-it": "Blazing fast text processing, long document summation, and creative writing.",
            "microsoft/phi-3-mini-128k-instruct": "Designed exclusively for reading and analyzing massive context windows.",
            "meta/llama-3.1-8b-instruct": "Generalist fallback for basic questions and simple conversations."
        }
        
        # Determine strict deterministic fallbacks to bypass API latency for obvious types:
        if analysis.get("tokens", 0) > 2000:
            return {
                "target_model": "microsoft/phi-3-mini-128k-instruct",
                "selection_reason": "Strength: Elite massive context aggregation. Assigned automatically due to 2000+ token payload."
            }
            
        routing_prompt = f"""You are the Master AI Router. Analyze the following user prompt and choose exactly ONE model from the list below that has the best strengths for the task.
        
MODELS & STRENGTHS:
1. meta/llama-3.1-405b-instruct : Best for dense advanced science/physics.
2. mistralai/mixtral-8x22b-instruct-v0.1 : Best for math, numbers, addition, equations.
3. qwen/qwen2.5-coder-32b-instruct : Best for writing code, python, HTML, JSON.
4. google/gemma-2-9b-it : Best for writing poems, summaries, translation, blogs.
5. meta/llama-3.1-8b-instruct : Best for simple 'hello', basic talk.

USER PROMPT: '{prompt_content[:500]}'

Reply strictly in valid JSON format with your chosen model and your reason why you picked it based on its strength:
{{"target_model": "model_string", "selection_reason": "Explain the exact strength and weakness that led to this decision."}}
"""

        # Perform the LLM inference directly to dynamically generate the decision!
        try:
            url = "https://integrate.api.nvidia.com/v1/chat/completions"
            api_key = getattr(settings, "NVIDIA_API_KEY", "")
            
            payload = {
                "model": "meta/llama3-70b-instruct",
                "messages": [{"role": "user", "content": routing_prompt}],
                "max_tokens": 150,
                "temperature": 0.1
            }
            headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
            response = requests.post(url, headers=headers, json=payload, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                content = data["choices"][0]["message"]["content"]
                
                # Parse the AI's literal JSON output
                start_idx = content.find('{')
                end_idx = content.rfind('}') + 1
                if start_idx != -1 and end_idx != -1:
                    ai_decision = json.loads(content[start_idx:end_idx])
                    
                    if ai_decision.get("target_model") in available_models:
                        return {
                            "target_model": ai_decision["target_model"],
                            "selection_reason": f"AI ROUTER DECISION: {ai_decision.get('selection_reason', 'dynamically selected.')}"
                        }
        except Exception as e:
            logger.warning(f"AI Router fell back to heuristic parsing: {e}")
            
        # Hard fallback dictionary if the LLM fails to respond in 3 seconds
        if "+" in prompt_content or "math" in prompt_content:
            return {"target_model": "mistralai/mixtral-8x22b-instruct-v0.1", "selection_reason": "Heuristic Mode: Fallback routed to MoE Math logic."}
        if "code" in prompt_content or "json" in prompt_content:
            return {"target_model": "qwen/qwen2.5-coder-32b-instruct", "selection_reason": "Heuristic Mode: Fallback routed to Qwen Coder."}
            
        return {
            "target_model": "google/gemma-2-9b-it",
            "selection_reason": "Heuristic Mode: Fallback mapped to fast generic classification node."
        }
