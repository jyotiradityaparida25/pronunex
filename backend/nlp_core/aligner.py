"""
Forced Alignment Module for Pronunex.

Uses Wav2Vec2 to align audio with expected phoneme sequence.
Reference: Adapted from Pronunex_initial_setup/src/get_timestamps.py
"""

import logging
from typing import List
import torch
import torchaudio
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor

logger = logging.getLogger(__name__)

# Singleton model instances (expensive to load)
_processor = None
_model = None


def get_alignment_model():
    """Get or load the Wav2Vec2 model for alignment."""
    global _processor, _model
    
    if _processor is None or _model is None:
        logger.info("Loading Wav2Vec2 alignment model...")
        _processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-base-960h")
        _model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")
        _model.eval()  # Set to evaluation mode
        logger.info("Wav2Vec2 model loaded successfully")
    
    return _processor, _model


def get_phoneme_timestamps(audio_path: str, expected_phonemes: List[str]) -> List[dict]:
    """
    Perform forced alignment to get phoneme timestamps.
    
    Args:
        audio_path: Path to cleaned audio file
        expected_phonemes: Expected ARPAbet phoneme sequence
    
    Returns:
        List of dicts with phoneme, start, and end times:
        [{"phoneme": "S", "start": 0.1, "end": 0.25}, ...]
    """
    processor, model = get_alignment_model()
    
    try:
        # Load audio
        waveform, sample_rate = torchaudio.load(audio_path)
        
        # Resample to 16kHz if needed (model requirement)
        if sample_rate != 16000:
            resampler = torchaudio.transforms.Resample(
                orig_freq=sample_rate, 
                new_freq=16000
            )
            waveform = resampler(waveform)
            sample_rate = 16000
        
        # Process audio
        input_values = processor(
            waveform.squeeze().numpy(), 
            return_tensors="pt", 
            sampling_rate=16000
        ).input_values
        
        # Get model predictions
        with torch.no_grad():
            logits = model(input_values).logits
        
        # Decode predictions to get character-level alignment
        pred_ids = torch.argmax(logits, dim=-1)
        
        # Calculate time per frame
        time_offset = model.config.inputs_to_logits_ratio / sample_rate
        
        # Extract timestamps for each character segment
        timestamps = extract_character_timestamps(
            pred_ids[0], 
            processor, 
            time_offset
        )
        
        # Map character timestamps to phoneme timestamps
        phoneme_timestamps = map_to_phonemes(timestamps, expected_phonemes)
        
        logger.debug(f"Aligned {len(phoneme_timestamps)} phonemes from audio")
        
        return phoneme_timestamps
        
    except Exception as e:
        logger.error(f"Alignment failed: {str(e)}")
        raise


def extract_character_timestamps(pred_ids, processor, time_offset: float) -> List[dict]:
    """
    Extract character-level timestamps from model predictions.
    
    Args:
        pred_ids: Predicted character IDs
        processor: Wav2Vec2 processor
        time_offset: Time per frame in seconds
    
    Returns:
        List of character timestamps
    """
    results = []
    current_char = ""
    start_time = 0
    
    for i, char_id in enumerate(pred_ids):
        char = processor.decode([char_id])
        
        if char != current_char:
            end_time = i * time_offset
            
            if current_char and current_char not in ["", "[PAD]", "|"]:
                results.append({
                    "char": current_char,
                    "start": start_time,
                    "end": end_time
                })
            
            current_char = char
            start_time = end_time
    
    # Handle last character
    if current_char and current_char not in ["", "[PAD]", "|"]:
        results.append({
            "char": current_char,
            "start": start_time,
            "end": len(pred_ids) * time_offset
        })
    
    return results


def map_to_phonemes(char_timestamps: List[dict], expected_phonemes: List[str]) -> List[dict]:
    """
    Map character-level timestamps to phoneme-level timestamps.
    
    This is a simplified mapping that distributes time across phonemes.
    For production, a more sophisticated alignment would be used.
    
    Args:
        char_timestamps: Character-level timestamps
        expected_phonemes: Expected phoneme sequence
    
    Returns:
        List of phoneme timestamps
    """
    if not char_timestamps or not expected_phonemes:
        return []
    
    # Get total duration
    if char_timestamps:
        total_duration = char_timestamps[-1]['end']
    else:
        total_duration = 0
    
    # Distribute time across phonemes proportionally
    phoneme_duration = total_duration / len(expected_phonemes) if expected_phonemes else 0
    
    result = []
    current_time = 0
    
    for i, phoneme in enumerate(expected_phonemes):
        result.append({
            "phoneme": phoneme,
            "start": round(current_time, 3),
            "end": round(current_time + phoneme_duration, 3),
            "index": i
        })
        current_time += phoneme_duration
    
    return result


def get_word_timestamps(audio_path: str, text: str) -> List[dict]:
    """
    Get word-level timestamps from audio.
    
    Args:
        audio_path: Path to audio file
        text: Transcription text
    
    Returns:
        List of word timestamps
    """
    processor, model = get_alignment_model()
    
    try:
        waveform, sample_rate = torchaudio.load(audio_path)
        
        if sample_rate != 16000:
            resampler = torchaudio.transforms.Resample(sample_rate, 16000)
            waveform = resampler(waveform)
            sample_rate = 16000
        
        input_values = processor(
            waveform.squeeze().numpy(),
            return_tensors="pt",
            sampling_rate=16000
        ).input_values
        
        with torch.no_grad():
            logits = model(input_values).logits
        
        pred_ids = torch.argmax(logits, dim=-1)
        transcription = processor.decode(pred_ids[0])
        
        time_offset = model.config.inputs_to_logits_ratio / sample_rate
        
        # Split transcription into words and estimate timestamps
        words = text.upper().split()
        total_duration = len(pred_ids[0]) * time_offset
        word_duration = total_duration / len(words) if words else 0
        
        result = []
        current_time = 0
        
        for word in words:
            result.append({
                "word": word,
                "start": round(current_time, 3),
                "end": round(current_time + word_duration, 3)
            })
            current_time += word_duration
        
        return result
        
    except Exception as e:
        logger.error(f"Word alignment failed: {str(e)}")
        raise
