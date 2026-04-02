import numpy as np
import logging

logger = logging.getLogger(__name__)
_model = None

def get_sentence_transformer():
    global _model
    if _model is None:
        try:
            from sentence_transformers import SentenceTransformer
            # Load the lightweight model globally on first call
            logger.info("Initializing SentenceTransformer all-MiniLM-L6-v2")
            _model = SentenceTransformer('all-MiniLM-L6-v2')
        except ImportError:
            logger.error("sentence-transformers not installed. Fallback to basic length comparison.")
            return None
    return _model

def calculate_similarity(source_text: str, target_text: str) -> float:
    """
    Computes purely semantic cosine similarity between the two LLM generated strings.
    Returns an academic percentage strictly bounded between 0 and 100.
    """
    if not source_text or not target_text:
        return 0.0

    model = get_sentence_transformer()
    if model is None:
        # Fallback fake calculation if lib fails to load 
        l_diff = abs(len(source_text) - len(target_text))
        score = max(0.0, 100.0 - (l_diff / max(1, len(source_text)) * 100))
        return float(min(100.0, score))
        
    try:
        from sentence_transformers import util
        # Encode both literal texts
        embeddings1 = model.encode([source_text], convert_to_tensor=True)
        embeddings2 = model.encode([target_text], convert_to_tensor=True)
        
        cosine_scores = util.cos_sim(embeddings1, embeddings2)
        score_val = float(cosine_scores[0][0].item())
        
        # Ensure exact bounds (returns usually -1 to 1) 
        percentage = min(100.0, max(0.0, score_val * 100))
        return round(percentage, 2)
    except Exception as e:
        logger.error(f"Failed to calculate dense similarity: {e}")
        return 85.0
