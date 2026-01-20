"""
Phoneme Extractor Module for Pronunex.

Converts text to phoneme sequences using Grapheme-to-Phoneme (G2P).
Reference: Adapted from Pronunex_initial_setup/src/generate_phonemes.py
"""

import logging
from typing import List, Tuple
from g2p_en import G2p

logger = logging.getLogger(__name__)

# Singleton G2P instance (expensive to initialize)
_g2p_instance = None


def get_g2p():
    """Get or create singleton G2P instance."""
    global _g2p_instance
    if _g2p_instance is None:
        logger.info("Initializing G2P model...")
        _g2p_instance = G2p()
    return _g2p_instance


def text_to_phonemes(text: str) -> List[str]:
    """
    Convert text to ARPAbet phoneme sequence.
    
    Args:
        text: Input text sentence
    
    Returns:
        List[str]: ARPAbet phoneme sequence, e.g., ['DH', 'AH0', 'K', 'W', 'IH1', 'K']
    """
    g2p = get_g2p()
    
    # Clean text
    text = text.strip().upper()
    
    # Convert to phonemes
    phonemes = g2p(text)
    
    # Filter out spaces and punctuation
    clean_phonemes = [p for p in phonemes if p.strip() and p not in [' ', ',', '.', '!', '?']]
    
    logger.debug(f"G2P: '{text}' -> {clean_phonemes}")
    
    return clean_phonemes


def text_to_phonemes_with_words(text: str) -> List[Tuple[str, List[str]]]:
    """
    Convert text to phoneme sequences with word boundaries.
    
    Args:
        text: Input text sentence
    
    Returns:
        List of tuples: [(word, [phonemes]), ...]
    """
    g2p = get_g2p()
    
    words = text.strip().split()
    result = []
    
    for word in words:
        # Clean word of punctuation
        clean_word = ''.join(c for c in word if c.isalnum())
        if clean_word:
            phonemes = g2p(clean_word)
            clean_phonemes = [p for p in phonemes if p.strip()]
            result.append((word, clean_phonemes))
    
    return result


def validate_phonemes_in_sentence(sentence: str, required_phonemes: List[str]) -> dict:
    """
    Validate that required phonemes exist in a sentence.
    Used to verify LLM-generated sentences.
    
    Args:
        sentence: Text sentence to validate
        required_phonemes: List of ARPAbet phonemes that must be present
    
    Returns:
        dict: {valid: bool, found: List[str], missing: List[str]}
    """
    sentence_phonemes = text_to_phonemes(sentence)
    
    # Remove stress markers for comparison (e.g., AH0 -> AH)
    normalized_sentence = [strip_stress(p) for p in sentence_phonemes]
    normalized_required = [strip_stress(p) for p in required_phonemes]
    
    found = []
    missing = []
    
    for phoneme in normalized_required:
        if phoneme in normalized_sentence:
            found.append(phoneme)
        else:
            missing.append(phoneme)
    
    return {
        'valid': len(missing) == 0,
        'found': found,
        'missing': missing,
        'sentence_phonemes': sentence_phonemes,
    }


def strip_stress(phoneme: str) -> str:
    """
    Remove stress markers from ARPAbet phoneme.
    
    E.g., 'AH0' -> 'AH', 'IY1' -> 'IY'
    """
    return ''.join(c for c in phoneme if not c.isdigit())


def get_phoneme_positions(word: str, phonemes: List[str]) -> List[dict]:
    """
    Determine position of each phoneme in a word (initial, medial, final).
    
    Args:
        word: The word being analyzed
        phonemes: Phonemes in the word
    
    Returns:
        List of dicts with phoneme and position
    """
    if not phonemes:
        return []
    
    result = []
    for i, phoneme in enumerate(phonemes):
        if i == 0:
            position = 'initial'
        elif i == len(phonemes) - 1:
            position = 'final'
        else:
            position = 'medial'
        
        result.append({
            'phoneme': phoneme,
            'position': position,
            'word': word,
        })
    
    return result
