"""
Feedback Generator for Pronunex.

Generates human-readable pronunciation feedback using LLM.

CRITICAL ARCHITECTURE CONSTRAINT:
- LLM receives PRE-COMPUTED scores
- LLM generates FEEDBACK TEXT only
- LLM does NOT score, detect, or evaluate pronunciation
"""

import logging
from typing import List
from services.llm_service import get_llm_service
from .prompt_templates import build_feedback_prompt
from .validators import validate_feedback_response

logger = logging.getLogger(__name__)


def generate_pronunciation_feedback(
    phoneme_scores: List[dict],
    weak_phonemes: List[str],
    sentence_text: str,
    overall_score: float
) -> dict:
    """
    Generate human-readable feedback for a pronunciation attempt.
    
    Args:
        phoneme_scores: Pre-computed phoneme scores from NLP core
        weak_phonemes: List of weak phoneme symbols
        sentence_text: The sentence that was practiced
        overall_score: Pre-computed overall score
    
    Returns:
        dict: {summary, phoneme_tips, encouragement, practice_focus}
    """
    try:
        # Build prompt with pre-computed scores
        prompt = build_feedback_prompt(
            sentence_text=sentence_text,
            overall_score=overall_score,
            weak_phonemes=weak_phonemes,
            phoneme_scores=phoneme_scores
        )
        
        # Call LLM service
        llm = get_llm_service()
        result = llm.generate(
            prompt=prompt,
            provider="auto",
            max_tokens=512,
            temperature=0.7,
            response_format="json"
        )
        
        if not result.get('success'):
            logger.warning("LLM generation failed, using fallback feedback")
            return generate_fallback_feedback(overall_score, weak_phonemes)
        
        feedback = result.get('content', {})
        
        # Validate LLM response
        validated = validate_feedback_response(feedback, weak_phonemes)
        
        logger.info(f"Generated feedback via {result.get('provider')}")
        
        return validated
        
    except Exception as e:
        logger.error(f"Feedback generation error: {str(e)}")
        return generate_fallback_feedback(overall_score, weak_phonemes)


def generate_fallback_feedback(overall_score: float, weak_phonemes: List[str]) -> dict:
    """
    Generate fallback feedback when LLM is unavailable.
    
    Uses rule-based templates instead of LLM.
    """
    # Determine performance level
    if overall_score >= 0.85:
        summary = "Excellent pronunciation! You have mastered most sounds in this sentence."
        encouragement = "Keep up the great work!"
    elif overall_score >= 0.7:
        summary = "Good pronunciation with room for improvement on some sounds."
        encouragement = "You are making solid progress. Focus on the weak sounds identified."
    elif overall_score >= 0.5:
        summary = "Fair pronunciation. Several sounds need more practice."
        encouragement = "With consistent practice, you will see improvement. Do not give up!"
    else:
        summary = "This sentence was challenging. Focus on the basic sounds first."
        encouragement = "Every expert was once a beginner. Keep practicing!"
    
    # Generate basic tips for weak phonemes
    phoneme_tips = []
    for phoneme in weak_phonemes[:3]:  # Limit to top 3
        tip = get_basic_articulation_tip(phoneme)
        if tip:
            phoneme_tips.append({
                'phoneme': phoneme,
                'tip': tip
            })
    
    return {
        'summary': summary,
        'phoneme_tips': phoneme_tips,
        'encouragement': encouragement,
        'practice_focus': weak_phonemes[:5],
    }


def get_basic_articulation_tip(phoneme: str) -> str:
    """
    Get a basic articulation tip for common phonemes.
    
    Used as fallback when LLM is unavailable.
    """
    tips = {
        'TH': "Place your tongue between your teeth and blow air gently.",
        'R': "Curl your tongue back slightly without touching the roof of your mouth.",
        'L': "Touch the tip of your tongue to the ridge behind your upper teeth.",
        'S': "Keep your tongue behind your teeth and let air flow through a narrow gap.",
        'Z': "Same as S, but add voice by vibrating your vocal cords.",
        'SH': "Round your lips slightly and push air through a wider channel than S.",
        'CH': "Start with your tongue touching the roof, then release with a SH sound.",
        'V': "Gently bite your lower lip and blow air while voicing.",
        'F': "Same position as V, but without voicing.",
        'W': "Round your lips into a small circle and glide into the next sound.",
        'NG': "Press the back of your tongue against your soft palate.",
        'AH': "Open your mouth wide with a relaxed tongue.",
        'EE': "Spread your lips and raise the front of your tongue.",
        'OO': "Round your lips and raise the back of your tongue.",
    }
    
    # Strip stress markers (e.g., AH0 -> AH)
    clean_phoneme = ''.join(c for c in phoneme if not c.isdigit())
    
    return tips.get(clean_phoneme, f"Practice the /{phoneme}/ sound in isolation before using it in words.")


def generate_articulation_tip(phoneme: str, phoneme_info: dict = None) -> dict:
    """
    Generate detailed articulation tip for a specific phoneme.
    
    Args:
        phoneme: ARPAbet phoneme symbol
        phoneme_info: Optional dict with type, example_word, etc.
    
    Returns:
        dict: {tip, practice_words}
    """
    from .prompt_templates import ARTICULATION_TIP_PROMPT
    
    try:
        llm = get_llm_service()
        
        prompt = ARTICULATION_TIP_PROMPT.format(
            phoneme=phoneme,
            phoneme_type=phoneme_info.get('type', 'consonant') if phoneme_info else 'consonant',
            example_word=phoneme_info.get('example_word', 'example') if phoneme_info else 'example',
            score=phoneme_info.get('score', 0.5) if phoneme_info else 0.5
        )
        
        result = llm.generate(prompt=prompt, max_tokens=256)
        
        if result.get('success'):
            return result.get('content', {})
        
    except Exception as e:
        logger.error(f"Articulation tip generation failed: {str(e)}")
    
    # Fallback
    return {
        'tip': get_basic_articulation_tip(phoneme),
        'practice_words': []
    }
