"""
Audio Slicer Module for Pronunex.

Slices audio into phoneme-level segments based on alignment timestamps.
Reference: Adapted from Pronunex_initial_setup/src/slice_audio.py
"""

import logging
from typing import List
import numpy as np
import librosa
from django.conf import settings

logger = logging.getLogger(__name__)


def slice_audio_by_timestamps(audio_path: str, timestamps: List[dict]) -> List[np.ndarray]:
    """
    Slice audio into segments based on phoneme timestamps.
    
    Args:
        audio_path: Path to cleaned audio file
        timestamps: List of phoneme timestamps from aligner
                   [{"phoneme": "S", "start": 0.1, "end": 0.25}, ...]
    
    Returns:
        List of numpy arrays, each containing audio for one phoneme
    """
    config = settings.SCORING_CONFIG
    sample_rate = config.get('SAMPLE_RATE', 16000)
    
    try:
        # Load audio
        y, sr = librosa.load(audio_path, sr=sample_rate)
        
        slices = []
        
        for ts in timestamps:
            start_sample = int(ts['start'] * sample_rate)
            end_sample = int(ts['end'] * sample_rate)
            
            # Ensure valid indices
            start_sample = max(0, start_sample)
            end_sample = min(len(y), end_sample)
            
            if start_sample < end_sample:
                audio_slice = y[start_sample:end_sample]
                slices.append(audio_slice)
            else:
                # Empty slice for missing phoneme
                slices.append(np.zeros(100))
        
        logger.debug(f"Created {len(slices)} audio slices from timestamps")
        
        return slices
        
    except Exception as e:
        logger.error(f"Audio slicing failed: {str(e)}")
        raise


def slice_and_save(audio_path: str, timestamps: List[dict], output_dir: str) -> List[str]:
    """
    Slice audio and save each segment to a file.
    
    Args:
        audio_path: Path to source audio
        timestamps: Phoneme timestamps
        output_dir: Directory to save slices
    
    Returns:
        List of paths to saved audio slices
    """
    import os
    import soundfile as sf
    
    config = settings.SCORING_CONFIG
    sample_rate = config.get('SAMPLE_RATE', 16000)
    
    os.makedirs(output_dir, exist_ok=True)
    
    slices = slice_audio_by_timestamps(audio_path, timestamps)
    saved_paths = []
    
    for i, (audio_slice, ts) in enumerate(zip(slices, timestamps)):
        phoneme = ts.get('phoneme', f'phoneme_{i}')
        filename = f"{i:03d}_{phoneme}.wav"
        filepath = os.path.join(output_dir, filename)
        
        sf.write(filepath, audio_slice, sample_rate)
        saved_paths.append(filepath)
    
    return saved_paths


def pad_or_trim_slice(audio_slice: np.ndarray, target_length: int) -> np.ndarray:
    """
    Pad or trim audio slice to target length.
    
    Useful for batch processing requiring consistent lengths.
    
    Args:
        audio_slice: Audio segment
        target_length: Target number of samples
    
    Returns:
        np.ndarray: Padded or trimmed audio
    """
    current_length = len(audio_slice)
    
    if current_length > target_length:
        # Trim from center
        start = (current_length - target_length) // 2
        return audio_slice[start:start + target_length]
    elif current_length < target_length:
        # Pad with zeros
        padding = target_length - current_length
        left_pad = padding // 2
        right_pad = padding - left_pad
        return np.pad(audio_slice, (left_pad, right_pad), mode='constant')
    else:
        return audio_slice


def extract_features_from_slice(audio_slice: np.ndarray, sample_rate: int = 16000) -> dict:
    """
    Extract audio features from a phoneme slice.
    
    Args:
        audio_slice: Audio segment
        sample_rate: Sample rate
    
    Returns:
        dict: Audio features (MFCC, pitch, energy)
    """
    # MFCC features
    mfcc = librosa.feature.mfcc(y=audio_slice, sr=sample_rate, n_mfcc=13)
    mfcc_mean = np.mean(mfcc, axis=1)
    
    # Energy (RMS)
    rms = librosa.feature.rms(y=audio_slice)
    energy = np.mean(rms)
    
    # Zero crossing rate
    zcr = librosa.feature.zero_crossing_rate(audio_slice)
    zcr_mean = np.mean(zcr)
    
    return {
        'mfcc': mfcc_mean.tolist(),
        'energy': float(energy),
        'zcr': float(zcr_mean),
        'duration': len(audio_slice) / sample_rate
    }
