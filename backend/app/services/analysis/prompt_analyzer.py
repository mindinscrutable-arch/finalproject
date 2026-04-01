from typing import Dict, Any

from app.services.analysis.provider_detector import ProviderDetector
from app.services.mapping.model_mapper import ModelMapper
from app.services.translation.openai_translator import OpenAITranslator
from app.services.translation.openai_translator import OpenAITranslator
from app.services.translation.model_selector import ModelSelector

class PromptAnalyzer:
    """
    Central brain for orchestrating the analysis, mapping, and translation of LLM prompts.
    """
    
    @staticmethod
    def analyze_and_translate(payload: Dict[str, Any], source_model: str) -> Dict[str, Any]:
        """
        Orchestrates the entire translation pipeline:
        1. Detects provider.
        2. Normalizes prompt payload.
        3. Maps the source model to the optimal Bedrock model.
        4. Formats the normalized prompt for the target Bedrock model.
        """
        # 1. Detect Provider based on the user-supplied source model
        provider = ProviderDetector.detect_from_model_name(source_model)
            
        # 2. Extract and Normalize Prompt Elements
        normalized_prompt = {}
        if provider == "openai":
            normalized_prompt = OpenAITranslator.extract_components(payload)
        # TODO: Add VertexTranslator, AzureTranslator, etc.
        else:
            # Fallback for unknown payloads, assume OpenAI-like for now as it's the most common
            normalized_prompt = OpenAITranslator.extract_components(payload)
            
        # 3. Map Model to Bedrock target
        mapped_model_info = ModelMapper.map_model(source_model, provider)
        
        # 4. Format for NVIDIA (NVIDIA NIMs support native OpenAI schema structure perfectly!)
        # We physically bypass the target-specific wrappers and pass standard dictionaries!
        # 4. Deep Prompt Analysis Engine
        prompt_content = ""
        for msg in normalized_prompt.get("messages", []):
            if isinstance(msg.get("content"), str):
                prompt_content += " " + msg["content"].lower()
                
        tokens_approx = len(prompt_content.split())
        
        analysis = {
            "type": "conversational",
            "complexity": "low",
            "tokens": tokens_approx,
            "requires_reasoning": False
        }
        
        # Extended Semantic Classification Dictionaries
        kw_coding = ["code", "python", "function", "bug", "script", "app", "html", "css", "javascript", "react", "sql", "debug", "compile"]
        kw_reasoning = ["explain", "why", "analyze", "math", "calculate", "equation", "physics", "solve", "+", "-", "=", "logic"]
        kw_summarization = ["summarize", "tldr", "abstract", "brief", "shorten", "reduce"]
        kw_creative = ["write", "blog", "poem", "email", "draft", "create", "story", "essay"]
        kw_data = ["json", "parse", "regex", "extract", "format", "csv", "table"]
        
        # Classifier Evaluation Engine
        if any(kw in prompt_content for kw in kw_coding):
            analysis["type"] = "coding"
            analysis["complexity"] = "high" if tokens_approx > 50 else "low"
            
        elif any(kw in prompt_content for kw in kw_data):
            analysis["type"] = "data_extraction"
            analysis["complexity"] = "high"
            
        elif any(kw in prompt_content for kw in kw_reasoning):
            analysis["type"] = "reasoning"
            analysis["requires_reasoning"] = True
            analysis["complexity"] = "high" if tokens_approx > 100 else "low"
            
        elif any(kw in prompt_content for kw in kw_summarization):
            analysis["type"] = "summarization"
            
        elif any(kw in prompt_content for kw in kw_creative):
            analysis["type"] = "creative"
            
        # 5. Format for NVIDIA (NVIDIA NIMs support native OpenAI schema structure perfectly!)
        nvidia_payload = {
            "messages": normalized_prompt.get("messages", [])
        }
        
        # 6. Invoke Dynamic AI Selection Engine
        selection_result = ModelSelector.select_best_model(analysis, prompt_content)
        target_model = selection_result["target_model"]
        selection_reason = selection_result["selection_reason"]
        
        return {
            "source": {
                "provider": provider,
                "model": source_model,
                "original_payload": payload,
                "detected_features": {
                    **analysis,
                    "has_system_prompt": bool(normalized_prompt.get("system")),
                    "is_json_mode": normalized_prompt.get("is_json_mode", False)
                }
            },
            "target": {
                "provider": "nvidia",
                "model": target_model,
                "mapping_reasons": [selection_reason],
                "bedrock_payload": nvidia_payload
            }
        }
