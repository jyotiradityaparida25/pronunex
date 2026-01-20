"""
Serializers for analytics data.
"""

from rest_framework import serializers
from .models import UserProgress, PhonemeProgress, StreakRecord


class UserProgressSerializer(serializers.ModelSerializer):
    """Serializer for daily progress data."""
    
    class Meta:
        model = UserProgress
        fields = [
            'date', 'sessions_count', 'total_practice_minutes',
            'attempts_count', 'average_score', 'best_score',
            'weak_phonemes', 'improved_phonemes'
        ]


class PhonemeProgressSerializer(serializers.ModelSerializer):
    """Serializer for per-phoneme progress."""
    
    phoneme_symbol = serializers.CharField(source='phoneme.symbol', read_only=True)
    phoneme_arpabet = serializers.CharField(source='phoneme.arpabet', read_only=True)
    is_weak = serializers.BooleanField(read_only=True)
    total_improvement = serializers.FloatField(read_only=True)
    
    class Meta:
        model = PhonemeProgress
        fields = [
            'phoneme_symbol', 'phoneme_arpabet', 'current_score',
            'attempts_count', 'first_attempt_score', 'best_score',
            'improvement_rate', 'is_weak', 'total_improvement',
            'first_practiced', 'last_practiced'
        ]


class StreakSerializer(serializers.ModelSerializer):
    """Serializer for streak data."""
    
    class Meta:
        model = StreakRecord
        fields = ['current_streak', 'longest_streak', 'last_practice_date']


class ProgressDashboardSerializer(serializers.Serializer):
    """Serializer for aggregated dashboard data."""
    
    # Summary stats
    total_sessions = serializers.IntegerField()
    total_attempts = serializers.IntegerField()
    total_practice_minutes = serializers.FloatField()
    overall_average_score = serializers.FloatField()
    
    # Current state
    current_weak_phonemes = serializers.ListField(child=serializers.CharField())
    current_strong_phonemes = serializers.ListField(child=serializers.CharField())
    
    # Trends
    score_trend = serializers.CharField()  # 'improving', 'stable', 'declining'
    recent_progress = UserProgressSerializer(many=True)
    
    # Streak
    streak = StreakSerializer()
    
    # Phoneme breakdown
    phoneme_progress = PhonemeProgressSerializer(many=True)
