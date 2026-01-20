"""
Vectorizer Module for Pronunex.

Converts audio slices to embedding vectors using Wav2Vec2.
These embeddings are used for pronunciation similarity scoring.
"""

import logging
from typing import List
import pickle
import numpy as np
import torch
import torchaudio
from transformers import Wav2Vec2Model, Wav2Vec2Processor
from django.conf import settings

logger = logging.getLogger(__name__)

# Singleton model for embedding generation
_embedding_processor = None
_embedding_model = None


def get_embedding_model():
    """Get or load the Wav2Vec2 model for embeddings."""
    global _embedding_processor, _embedding_model
    
    if _embedding_processor is None or _embedding_model is None:
        logger.info("Loading Wav2Vec2 embedding model...")
        _embedding_processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-base-960h")
        _embedding_model = Wav2Vec2Model.from_pretrained("facebook/wav2vec2-base-960h")
        _embedding_model.eval()
        logger.info("Wav2Vec2 embedding model loaded")
    
    return _embedding_processor, _embedding_model


def audio_to_embedding(audio_slice: np.ndarray, sample_rate: int = 16000) -> np.ndarray:
    """
    Convert a single audio slice to an embedding vector.
    
    Args:
        audio_slice: Audio waveform as numpy array
        sample_rate: Sample rate (default 16kHz)
    
    Returns:
        np.ndarray: 768-dimensional embedding vector
    """
    processor, model = get_embedding_model()
    
    try:
        # Ensure minimum length for processing
        if len(audio_slice) < 400:
            audio_slice = np.pad(audio_slice, (0, 400 - len(audio_slice)))
        
        # Process audio
        inputs = processor(
            audio_slice.astype(np.float32), 
            sampling_rate=sample_rate, 
            return_tensors="pt",
            padding=True
        )
        
        with torch.no_grad():
            outputs = model(**inputs)
            # Get the mean of hidden states as embedding
            hidden_states = outputs.last_hidden_state
            embedding = torch.mean(hidden_states, dim=1).squeeze().numpy()
        
        return embedding
        
    except Exception as e:
        logger.error(f"Embedding generation failed: {str(e)}")
        # Return zero vector on failure
        return np.zeros(settings.SCORING_CONFIG.get('EMBEDDING_DIM', 768))


def batch_audio_to_embeddings(audio_slices: List[np.ndarray]) -> List[np.ndarray]:
    """
    Convert multiple audio slices to embeddings.
    
    Args:
        audio_slices: List of audio waveforms
    
    Returns:
        List of embedding vectors
    """
    embeddings = []
    
    for i, audio_slice in enumerate(audio_slices):
        try:
            embedding = audio_to_embedding(audio_slice)
            embeddings.append(embedding)
        except Exception as e:
            logger.warning(f"Failed to embed slice {i}: {str(e)}")
            embeddings.append(np.zeros(settings.SCORING_CONFIG.get('EMBEDDING_DIM', 768)))
    
    return embeddings


def compute_sentence_embedding(audio_path: str, sample_rate: int = 16000) -> np.ndarray:
    """
    Compute a single embedding for an entire audio file.
    
    This is used when phoneme-level alignment is not available.
    Generates one embedding representing the full sentence pronunciation.
    
    Args:
        audio_path: Path to audio file
        sample_rate: Target sample rate (default 16kHz)
    
    Returns:
        np.ndarray: 768-dimensional embedding vector
    """
    import librosa
    
    # Load audio file
    try:
        audio, sr = librosa.load(audio_path, sr=sample_rate)
    except Exception as e:
        logger.error(f"Failed to load audio for embedding: {str(e)}")
        return np.zeros(settings.SCORING_CONFIG.get('EMBEDDING_DIM', 768))
    
    # Compute embedding from full audio
    return audio_to_embedding(audio, sample_rate)


def compute_reference_embeddings(sentence) -> List[np.ndarray]:
    """
    Compute reference embeddings for a sentence.
    
    This should be run during data seeding, not during assessment.
    
    Args:
        sentence: ReferenceSentence model instance
    
    Returns:
        List of embedding vectors for each phoneme
    """
    from .audio_cleaner import clean_audio
    from .audio_slicer import slice_audio_by_timestamps
    
    audio_source = sentence.get_audio_source()
    if not audio_source:
        raise ValueError("Sentence has no audio source")
    
    # Clean the reference audio
    cleaned_path = clean_audio(audio_source)
    
    # Get timestamps from alignment map
    timestamps = sentence.alignment_map
    
    # Slice audio
    slices = slice_audio_by_timestamps(cleaned_path, timestamps)
    
    # Generate embeddings
    embeddings = batch_audio_to_embeddings(slices)
    
    return embeddings


def serialize_embeddings(embeddings: List[np.ndarray]) -> bytes:
    """
    Serialize embeddings for database storage.
    
    Args:
        embeddings: List of numpy arrays
    
    Returns:
        bytes: Pickled embeddings
    """
    return pickle.dumps(embeddings)


def deserialize_embeddings(data: bytes) -> List[np.ndarray]:
    """
    Deserialize embeddings from database.
    
    Args:
        data: Pickled embeddings
    
    Returns:
        List of numpy arrays
    """
    return pickle.loads(data)


def embedding_distance(emb1: np.ndarray, emb2: np.ndarray, metric: str = 'cosine') -> float:
    """
    Calculate distance between two embeddings.
    
    Args:
        emb1: First embedding
        emb2: Second embedding
        metric: Distance metric ('cosine' or 'euclidean')
    
    Returns:
        float: Distance value
    """
    if metric == 'cosine':
        # Cosine distance (1 - cosine similarity)
        from scipy.spatial.distance import cosine
        return cosine(emb1, emb2)
    elif metric == 'euclidean':
        return np.linalg.norm(emb1 - emb2)
    else:
        raise ValueError(f"Unknown metric: {metric}")
