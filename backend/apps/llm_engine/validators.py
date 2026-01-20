"""
Validators for LLM Output.

Validates and sanitizes LLM responses before use.
Ensures output structure matches expected format.
"""

import logging
from typing import List

logger = logging.getLogger(__name__)


def validate_feedback_response(response: dict, weak_phonemes: List[str]) -> dict:
    """
    Validate and sanitize LLM feedback response.
    
    Ensures:
    1. All required fields are present
    2. phoneme_tips reference valid weak phonemes
    3. No unexpected content
    
    Args:
        response: Raw LLM response dict
        weak_phonemes: List of weak phonemes to validate against
    
    Returns:
        dict: Validated and sanitized feedback
    """
    validated = {}
    
    # Validate summary
    validated['summary'] = response.get('summary', 'Assessment complete.')
    if not isinstance(validated['summary'], str):
        validated['summary'] = str(validated['summary'])
    
    # Validate and filter phoneme tips
    raw_tips = response.get('phoneme_tips', [])
    validated['phoneme_tips'] = []
    
    if isinstance(raw_tips, list):
        for tip in raw_tips:
            if isinstance(tip, dict) and 'phoneme' in tip and 'tip' in tip:
                validated['phoneme_tips'].append({
                    'phoneme': str(tip['phoneme']),
                    'tip': str(tip['tip'])
                })
    
    # Validate encouragement
    validated['encouragement'] = response.get(
        'encouragement', 
        'Keep practicing to improve your pronunciation.'
    )
    if not isinstance(validated['encouragement'], str):
        validated['encouragement'] = str(validated['encouragement'])
    
    # Validate practice focus
    raw_focus = response.get('practice_focus', weak_phonemes)
    validated['practice_focus'] = []
    
    if isinstance(raw_focus, list):
        for item in raw_focus:
            if isinstance(item, str):
                validated['practice_focus'].append(item)
    
    # Fallback if practice_focus is empty
    if not validated['practice_focus']:
        validated['practice_focus'] = weak_phonemes[:5]
    
    return validated


def validate_sentence_response(response: dict, required_phonemes: List[str]) -> dict:
    """
    Validate LLM-generated sentence response.
    
    Verifies:
    1. Sentence contains required phonemes (via G2P)
    2. Response has expected structure
    3. Sentence is reasonable length
    
    Args:
        response: Raw LLM response
        required_phonemes: Phonemes that must be in sentence
    
    Returns:
        dict: Validated response with validation status
    """
    validated = {
        'valid': False,
        'sentence': '',
        'target_words': [],
        'validation_errors': [],
    }
    
    # Check sentence
    sentence = response.get('sentence', '')
    if not sentence or not isinstance(sentence, str):
        validated['validation_errors'].append('Missing or invalid sentence')
        return validated
    
    validated['sentence'] = sentence.strip()
    
    # Verify phonemes using G2P
    from nlp_core.phoneme_extractor import validate_phonemes_in_sentence
    
    phoneme_check = validate_phonemes_in_sentence(sentence, required_phonemes)
    
    if not phoneme_check['valid']:
        validated['validation_errors'].append(
            f"Missing phonemes: {', '.join(phoneme_check['missing'])}"
        )
        return validated
    
    # Validate target words
    raw_words = response.get('target_words', [])
    if isinstance(raw_words, list):
        for word_info in raw_words:
            if isinstance(word_info, dict):
                validated['target_words'].append({
                    'word': str(word_info.get('word', '')),
                    'phoneme': str(word_info.get('phoneme', ''))
                })
    
    # Check sentence length
    word_count = len(sentence.split())
    if word_count < 3:
        validated['validation_errors'].append('Sentence too short')
        return validated
    
    if word_count > 20:
        validated['validation_errors'].append('Sentence too long')
        return validated
    
    validated['valid'] = True
    validated['phoneme_verification'] = phoneme_check
    
    return validated


def validate_coaching_response(response: str) -> dict:
    """
    Validate coaching/chat response.
    
    Ensures response is appropriate and not harmful.
    
    Args:
        response: Raw text response from LLM
    
    Returns:
        dict: Validated response
    """
    if not response or not isinstance(response, str):
        return {
            'valid': False,
            'content': 'I am sorry, I could not generate a response. Please try again.',
        }
    
    # Basic content filtering
    response = response.strip()
    
    # Length check
    if len(response) > 2000:
        response = response[:2000] + '...'
    
    return {
        'valid': True,
        'content': response,
    }


def sanitize_text(text: str) -> str:
    """
    Sanitize text for safe storage and display.
    
    Removes potentially harmful content.
    """
    if not isinstance(text, str):
        return ''
    
    # Basic sanitization
    text = text.strip()
    
    # Remove control characters
    text = ''.join(char for char in text if ord(char) >= 32 or char in '\n\t')
    
    return text
