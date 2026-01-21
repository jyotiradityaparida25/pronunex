"""
URL patterns for analytics endpoints.
"""

from django.urls import path
from .views import (
    ProgressDashboardView,
    PhonemeAnalyticsView,
    WeakPhonemesView,
    HistoryView,
)

urlpatterns = [
    path('analytics/progress/', ProgressDashboardView.as_view(), name='progress_dashboard'),
    path('analytics/phoneme-stats/', PhonemeAnalyticsView.as_view(), name='phoneme_stats'),
    path('analytics/weak-phonemes/', WeakPhonemesView.as_view(), name='weak_phonemes'),
    path('analytics/history/', HistoryView.as_view(), name='progress_history'),
]
