from django.contrib import admin
from .models import UserSession, Attempt, PhonemeError


class AttemptInline(admin.TabularInline):
    model = Attempt
    extra = 0
    readonly_fields = ['score', 'fluency_score', 'created_at']
    fields = ['sentence', 'score', 'fluency_score', 'created_at']


@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    list_display = ['user', 'session_type', 'overall_score', 'total_attempts', 'started_at', 'ended_at']
    list_filter = ['session_type', 'started_at']
    search_fields = ['user__email']
    readonly_fields = ['started_at', 'overall_score', 'total_attempts']
    inlines = [AttemptInline]


class PhonemeErrorInline(admin.TabularInline):
    model = PhonemeError
    extra = 0
    readonly_fields = ['target_phoneme', 'similarity_score', 'word_context']
    fields = ['target_phoneme', 'similarity_score', 'word_context', 'position_in_word']


@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    list_display = ['session', 'sentence_preview', 'score', 'fluency_score', 'created_at']
    list_filter = ['session__session_type', 'created_at']
    search_fields = ['session__user__email', 'sentence__text']
    readonly_fields = ['score', 'fluency_score', 'phoneme_scores', 'llm_feedback', 'processing_time_ms', 'created_at']
    inlines = [PhonemeErrorInline]
    
    def sentence_preview(self, obj):
        return obj.sentence.text[:40] + '...' if len(obj.sentence.text) > 40 else obj.sentence.text
    sentence_preview.short_description = 'Sentence'


@admin.register(PhonemeError)
class PhonemeErrorAdmin(admin.ModelAdmin):
    list_display = ['target_phoneme', 'similarity_score', 'word_context', 'position_in_word', 'is_weak_display']
    list_filter = ['position_in_word', 'target_phoneme']
    search_fields = ['word_context', 'attempt__session__user__email']
    
    def is_weak_display(self, obj):
        return obj.is_weak
    is_weak_display.boolean = True
    is_weak_display.short_description = 'Weak'
