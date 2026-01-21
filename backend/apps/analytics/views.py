"""
API Views for analytics and progress tracking.
"""

import logging
from datetime import timedelta
from django.utils import timezone
from django.db.models import Avg, Count, Max, Min, Sum
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import UserProgress, PhonemeProgress, StreakRecord
from .serializers import (
    UserProgressSerializer,
    PhonemeProgressSerializer,
    StreakSerializer,
    ProgressDashboardSerializer,
)
from apps.practice.models import Attempt, UserSession, PhonemeError

logger = logging.getLogger(__name__)


class ProgressDashboardView(APIView):
    """
    GET /api/v1/analytics/progress/
    
    Get comprehensive progress dashboard data.
    """
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        days = int(request.query_params.get('days', 30))
        
        # Calculate date range
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=days)
        
        # Get aggregated stats
        session_stats = UserSession.objects.filter(
            user=user
        ).aggregate(
            total_sessions=Count('id'),
            total_minutes=Sum('overall_score')  # This should be duration
        )
        
        attempt_stats = Attempt.objects.filter(
            session__user=user
        ).aggregate(
            total_attempts=Count('id'),
            avg_score=Avg('score'),
            best_score=Max('score'),
        )
        
        # Get recent daily progress
        recent_progress = UserProgress.objects.filter(
            user=user,
            date__gte=start_date,
            date__lte=end_date
        ).order_by('-date')[:days]
        
        # Get phoneme progress
        phoneme_progress = PhonemeProgress.objects.filter(
            user=user
        ).select_related('phoneme').order_by('-current_score')
        
        # Identify weak and strong phonemes
        from django.conf import settings
        threshold = settings.SCORING_CONFIG.get('WEAK_PHONEME_THRESHOLD', 0.7)
        
        weak_phonemes = [
            pp.phoneme.arpabet 
            for pp in phoneme_progress 
            if pp.current_score < threshold
        ]
        
        strong_phonemes = [
            pp.phoneme.arpabet 
            for pp in phoneme_progress 
            if pp.current_score >= 0.85
        ]
        
        # Calculate score trend
        if len(recent_progress) >= 3:
            recent_scores = [rp.average_score for rp in recent_progress[:3] if rp.average_score]
            older_scores = [rp.average_score for rp in recent_progress[3:6] if rp.average_score]
            
            if recent_scores and older_scores:
                recent_avg = sum(recent_scores) / len(recent_scores)
                older_avg = sum(older_scores) / len(older_scores)
                
                if recent_avg > older_avg + 0.05:
                    score_trend = 'improving'
                elif recent_avg < older_avg - 0.05:
                    score_trend = 'declining'
                else:
                    score_trend = 'stable'
            else:
                score_trend = 'insufficient_data'
        else:
            score_trend = 'insufficient_data'
        
        # Get or create streak
        streak, _ = StreakRecord.objects.get_or_create(user=user)
        
        # Calculate practice minutes
        total_minutes = 0
        for progress in recent_progress:
            total_minutes += progress.total_practice_minutes
        
        response_data = {
            'total_sessions': session_stats.get('total_sessions', 0),
            'total_attempts': attempt_stats.get('total_attempts', 0),
            'total_practice_minutes': round(total_minutes, 1),
            'overall_average_score': round(attempt_stats.get('avg_score', 0) or 0, 2),
            'current_weak_phonemes': weak_phonemes[:10],
            'current_strong_phonemes': strong_phonemes[:10],
            'score_trend': score_trend,
            'recent_progress': UserProgressSerializer(recent_progress, many=True).data,
            'streak': StreakSerializer(streak).data,
            'phoneme_progress': PhonemeProgressSerializer(phoneme_progress, many=True).data,
        }
        
        return Response(response_data)


class PhonemeAnalyticsView(APIView):
    """
    GET /api/v1/analytics/phonemes/
    
    Get detailed per-phoneme analytics.
    """
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        
        # Get all phoneme progress records
        phoneme_progress = PhonemeProgress.objects.filter(
            user=user
        ).select_related('phoneme').order_by('phoneme__type', 'phoneme__arpabet')
        
        # Group by phoneme type
        by_type = {}
        for pp in phoneme_progress:
            ptype = pp.phoneme.type
            if ptype not in by_type:
                by_type[ptype] = []
            by_type[ptype].append(PhonemeProgressSerializer(pp).data)
        
        # Get weak phonemes with error context
        from django.conf import settings
        threshold = settings.SCORING_CONFIG.get('WEAK_PHONEME_THRESHOLD', 0.7)
        
        weak_details = []
        for pp in phoneme_progress.filter(current_score__lt=threshold):
            # Get common error contexts
            errors = PhonemeError.objects.filter(
                attempt__session__user=user,
                target_phoneme=pp.phoneme
            ).values('word_context', 'position_in_word').annotate(
                count=Count('id'),
                avg_score=Avg('similarity_score')
            ).order_by('-count')[:5]
            
            weak_details.append({
                'phoneme': pp.phoneme.arpabet,
                'symbol': pp.phoneme.symbol,
                'current_score': pp.current_score,
                'attempts': pp.attempts_count,
                'common_errors': list(errors),
            })
        
        return Response({
            'by_type': by_type,
            'weak_phonemes_detail': weak_details,
            'total_phonemes_practiced': phoneme_progress.count(),
        })


class HistoryView(generics.ListAPIView):
    """
    GET /api/v1/analytics/history/
    
    Get daily progress history.
    """
    
    serializer_class = UserProgressSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        days = int(self.request.query_params.get('days', 30))
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=days)
        
        return UserProgress.objects.filter(
            user=self.request.user,
            date__gte=start_date,
            date__lte=end_date
        ).order_by('-date')


class WeakPhonemesView(APIView):
    """
    GET /api/v1/analytics/weak-phonemes/
    
    Get list of user's current weak phonemes.
    """
    
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        from django.conf import settings
        threshold = settings.SCORING_CONFIG.get('WEAK_PHONEME_THRESHOLD', 0.7)
        
        phoneme_progress = PhonemeProgress.objects.filter(
            user=user,
            current_score__lt=threshold
        ).select_related('phoneme').order_by('current_score')
        
        weak_phonemes = [
            {
                'phoneme': pp.phoneme.arpabet,
                'symbol': pp.phoneme.symbol,
                'score': round(pp.current_score, 2),
                'attempts': pp.attempts_count,
            }
            for pp in phoneme_progress
        ]
        
        return Response({
            'weak_phonemes': weak_phonemes,
            'threshold': threshold,
            'count': len(weak_phonemes),
        })


def update_user_analytics(user, attempt):
    """
    Update analytics after a new attempt.
    Called from assessment service.
    """
    today = timezone.now().date()
    
    # Update daily progress
    progress, created = UserProgress.objects.get_or_create(
        user=user,
        date=today,
        defaults={
            'sessions_count': 0,
            'attempts_count': 0,
            'average_score': 0,
        }
    )
    
    # Update attempt count and score
    progress.attempts_count += 1
    
    # Recalculate average
    all_today = Attempt.objects.filter(
        session__user=user,
        created_at__date=today
    ).aggregate(avg=Avg('score'), best=Max('score'))
    
    progress.average_score = all_today.get('avg', 0)
    progress.best_score = all_today.get('best', 0)
    progress.save()
    
    # Update phoneme progress
    for error in attempt.phoneme_errors.all():
        phoneme_prog, _ = PhonemeProgress.objects.get_or_create(
            user=user,
            phoneme=error.target_phoneme,
            defaults={'first_practiced': timezone.now()}
        )
        
        # Update scores
        phoneme_prog.attempts_count += 1
        phoneme_prog.last_practiced = timezone.now()
        
        if phoneme_prog.first_attempt_score is None:
            phoneme_prog.first_attempt_score = error.similarity_score
        
        if phoneme_prog.best_score is None or error.similarity_score > phoneme_prog.best_score:
            phoneme_prog.best_score = error.similarity_score
        
        # Calculate current score as recent average
        recent_errors = PhonemeError.objects.filter(
            attempt__session__user=user,
            target_phoneme=error.target_phoneme
        ).order_by('-attempt__created_at')[:10]
        
        if recent_errors:
            phoneme_prog.current_score = sum(
                e.similarity_score for e in recent_errors
            ) / len(recent_errors)
        
        phoneme_prog.save()
    
    # Update streak
    streak, _ = StreakRecord.objects.get_or_create(user=user)
    
    if streak.last_practice_date:
        if streak.last_practice_date == today:
            pass  # Already practiced today
        elif streak.last_practice_date == today - timedelta(days=1):
            streak.current_streak += 1
        else:
            streak.current_streak = 1  # Reset streak
    else:
        streak.current_streak = 1
    
    streak.last_practice_date = today
    
    if streak.current_streak > streak.longest_streak:
        streak.longest_streak = streak.current_streak
    
    streak.save()
