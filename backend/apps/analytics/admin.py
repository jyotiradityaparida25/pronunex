from django.contrib import admin
from .models import UserProgress, PhonemeProgress, StreakRecord


@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'attempts_count', 'average_score', 'best_score']
    list_filter = ['date']
    search_fields = ['user__email']
    ordering = ['-date']
    date_hierarchy = 'date'


@admin.register(PhonemeProgress)
class PhonemeProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'phoneme', 'current_score', 'attempts_count', 'improvement_rate']
    list_filter = ['phoneme__type']
    search_fields = ['user__email', 'phoneme__arpabet']
    ordering = ['user', 'phoneme']


@admin.register(StreakRecord)
class StreakRecordAdmin(admin.ModelAdmin):
    list_display = ['user', 'current_streak', 'longest_streak', 'last_practice_date']
    search_fields = ['user__email']
