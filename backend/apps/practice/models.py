"""
Practice Models for Pronunex.

Contains user practice data: sessions, attempts, and phoneme-level errors.
"""

from django.db import models
from django.conf import settings


class UserSession(models.Model):
    """
    Practice session grouping multiple attempts.
    Tracks session-level metrics and timing.
    """
    
    SESSION_TYPE_CHOICES = [
        ('practice', 'Practice'),
        ('assessment', 'Assessment'),
        ('warmup', 'Warmup'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='practice_sessions'
    )
    session_type = models.CharField(
        max_length=20, 
        choices=SESSION_TYPE_CHOICES,
        default='practice'
    )
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    
    # Session-level metrics (computed from attempts)
    overall_score = models.FloatField(null=True, blank=True)
    total_attempts = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = 'User Session'
        verbose_name_plural = 'User Sessions'
        ordering = ['-started_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.session_type} ({self.started_at.date()})"
    
    def calculate_overall_score(self):
        """Calculate average score from all attempts in session."""
        attempts = self.attempts.all()
        if attempts.exists():
            avg = attempts.aggregate(models.Avg('score'))['score__avg']
            self.overall_score = round(avg, 2) if avg else None
            self.total_attempts = attempts.count()
            self.save()


class Attempt(models.Model):
    """
    Single pronunciation attempt for a reference sentence.
    
    Stores user audio, computed scores, and LLM-generated feedback.
    """
    
    session = models.ForeignKey(
        UserSession, 
        on_delete=models.CASCADE,
        related_name='attempts'
    )
    sentence = models.ForeignKey(
        'library.ReferenceSentence', 
        on_delete=models.CASCADE,
        related_name='user_attempts'
    )
    
    # User audio storage
    audio_file = models.FileField(upload_to='user_uploads/', blank=True, null=True)
    audio_url = models.URLField(blank=True, help_text='Supabase storage URL')
    
    # Computed scores (deterministic, not LLM-based)
    score = models.FloatField(help_text='Overall pronunciation score (0-1)')
    fluency_score = models.FloatField(
        null=True, 
        blank=True,
        help_text='Fluency/timing score (0-1)'
    )
    
    # Detailed phoneme-level results
    phoneme_scores = models.JSONField(
        null=True,
        blank=True,
        help_text='Per-phoneme scores: [{"phoneme": "S", "score": 0.92}]'
    )
    
    # LLM-generated feedback (interpretation only, not scoring)
    llm_feedback = models.JSONField(
        null=True, 
        blank=True,
        help_text='LLM feedback: {summary, phoneme_tips, encouragement}'
    )
    
    # Metadata
    processing_time_ms = models.IntegerField(
        null=True, 
        blank=True,
        help_text='Total processing time in milliseconds'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Attempt'
        verbose_name_plural = 'Attempts'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Attempt on '{self.sentence.text[:30]}...' - {self.score:.2f}"


class PhonemeError(models.Model):
    """
    Records individual phoneme-level errors for an attempt.
    
    Critical for:
    - Identifying user's weak phonemes
    - Driving personalized recommendations
    - Tracking improvement over time
    """
    
    POSITION_CHOICES = [
        ('initial', 'Initial'),
        ('medial', 'Medial'),
        ('final', 'Final'),
    ]
    
    attempt = models.ForeignKey(
        Attempt, 
        on_delete=models.CASCADE,
        related_name='phoneme_errors'
    )
    target_phoneme = models.ForeignKey(
        'library.Phoneme', 
        on_delete=models.CASCADE,
        related_name='user_errors'
    )
    
    # Embedding comparison data
    expected_vector = models.BinaryField(
        null=True, 
        blank=True,
        help_text='Reference phoneme embedding (serialized numpy)'
    )
    user_vector = models.BinaryField(
        null=True, 
        blank=True,
        help_text='User pronunciation embedding (serialized numpy)'
    )
    
    # Similarity score (determines if error)
    similarity_score = models.FloatField(help_text='Cosine similarity (0-1)')
    
    # Context information
    word_context = models.CharField(
        max_length=100,
        help_text='Word containing the phoneme'
    )
    position_in_word = models.CharField(
        max_length=20,
        choices=POSITION_CHOICES,
        default='medial'
    )
    
    # Timestamp in audio
    start_time = models.FloatField(
        null=True, 
        blank=True,
        help_text='Start time in audio (seconds)'
    )
    end_time = models.FloatField(
        null=True, 
        blank=True,
        help_text='End time in audio (seconds)'
    )
    
    class Meta:
        verbose_name = 'Phoneme Error'
        verbose_name_plural = 'Phoneme Errors'
        ordering = ['attempt', 'start_time']
    
    def __str__(self):
        return f"/{self.target_phoneme.arpabet}/ in '{self.word_context}' - {self.similarity_score:.2f}"
    
    @property
    def is_weak(self):
        """Check if score is below configurable threshold."""
        threshold = settings.SCORING_CONFIG.get('WEAK_PHONEME_THRESHOLD', 0.7)
        return self.similarity_score < threshold
