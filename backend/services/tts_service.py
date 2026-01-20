"""
Text-to-Speech Service for Pronunex.

Uses Groq Orpheus model to generate reference pronunciation audio.
Audio is cached to avoid repeated API calls.
"""

import os
import logging
from pathlib import Path
from django.conf import settings

logger = logging.getLogger(__name__)


class TTSService:
    """
    TTS service using Groq Orpheus for reference audio generation.
    """
    
    def __init__(self):
        self.api_key = settings.GROQ_API_KEY
        self.model = "canopylabs/orpheus-v1-english"
        self.voice = "diana"  # Clear female voice for pronunciation
        self.client = None
        self._init_client()
    
    def _init_client(self):
        """Initialize Groq client."""
        if not self.api_key:
            logger.warning("GROQ_API_KEY not set, TTS will not work")
            return
        
        try:
            from groq import Groq
            self.client = Groq(api_key=self.api_key)
            logger.info("Groq TTS client initialized")
        except ImportError:
            logger.error("groq package not installed")
        except Exception as e:
            logger.error(f"Failed to initialize Groq client: {str(e)}")
    
    def generate_audio(self, text: str, output_path: str = None, voice: str = None) -> str:
        """
        Generate speech audio from text using Groq Orpheus.
        
        Args:
            text: Text to convert to speech (max 200 chars)
            output_path: Optional path to save audio file
            voice: Optional voice override (diana, troy, hannah, austin, daniel, autumn)
        
        Returns:
            str: Path to generated audio file
        """
        if not self.client:
            raise ValueError("TTS client not initialized. Check GROQ_API_KEY.")
        
        # Truncate text if too long (API limit is 200 chars)
        if len(text) > 200:
            text = text[:197] + "..."
            logger.warning(f"Text truncated to 200 chars for TTS")
        
        voice = voice or self.voice
        
        try:
            # Generate speech
            response = self.client.audio.speech.create(
                model=self.model,
                voice=voice,
                input=text,
                response_format="wav"
            )
            
            # Determine output path
            if output_path is None:
                media_dir = Path(settings.MEDIA_ROOT) / 'references'
                media_dir.mkdir(parents=True, exist_ok=True)
                
                # Create filename from text hash
                import hashlib
                text_hash = hashlib.md5(text.encode()).hexdigest()[:12]
                output_path = str(media_dir / f"tts_{text_hash}.wav")
            
            # Save to file
            response.write_to_file(output_path)
            
            logger.info(f"TTS audio generated: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"TTS generation failed: {str(e)}")
            raise
    
    def generate_for_sentence(self, sentence) -> str:
        """
        Generate reference audio for a ReferenceSentence model instance.
        
        Args:
            sentence: ReferenceSentence model instance
        
        Returns:
            str: Path to generated audio file
        """
        # Create unique filename based on sentence ID
        media_dir = Path(settings.MEDIA_ROOT) / 'references'
        media_dir.mkdir(parents=True, exist_ok=True)
        
        output_path = str(media_dir / f"sentence_{sentence.id}.wav")
        
        # Generate audio
        return self.generate_audio(
            text=sentence.text,
            output_path=output_path
        )


# Singleton instance
_tts_service = None


def get_tts_service() -> TTSService:
    """Get or create singleton TTS service."""
    global _tts_service
    if _tts_service is None:
        _tts_service = TTSService()
    return _tts_service


def generate_sentence_audio(sentence) -> str:
    """
    Convenience function to generate audio for a sentence.
    
    Args:
        sentence: ReferenceSentence model instance
    
    Returns:
        str: Path to audio file
    """
    service = get_tts_service()
    return service.generate_for_sentence(sentence)
