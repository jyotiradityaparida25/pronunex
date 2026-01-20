"""
URL patterns for analytics endpoints.
"""

from django.urls import path
from .views import (
    ProgressDashboardView,
    PhonemeAnalyticsView,
    HistoryView,
)

urlpatterns = [
    path('analytics/progress/', ProgressDashboardView.as_view(), name='progress_dashboard'),
    path('analytics/phonemes/', PhonemeAnalyticsView.as_view(), name='phoneme_analytics'),
    path('analytics/history/', HistoryView.as_view(), name='progress_history'),
]
