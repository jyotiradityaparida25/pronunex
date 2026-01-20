"""
URL patterns for practice endpoints.
"""

from django.urls import path
from .views import (
    UserSessionListView,
    UserSessionDetailView,
    EndSessionView,
    AttemptListView,
    AttemptDetailView,
    AssessmentView,
)

urlpatterns = [
    # Sessions
    path('sessions/', UserSessionListView.as_view(), name='session_list'),
    path('sessions/<int:pk>/', UserSessionDetailView.as_view(), name='session_detail'),
    path('sessions/<int:pk>/end/', EndSessionView.as_view(), name='session_end'),
    
    # Attempts
    path('attempts/', AttemptListView.as_view(), name='attempt_list'),
    path('attempts/<int:pk>/', AttemptDetailView.as_view(), name='attempt_detail'),
    
    # Core Assessment
    path('assess/', AssessmentView.as_view(), name='assess'),
]
