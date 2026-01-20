from django.contrib import admin
from .models import Phoneme, ReferenceSentence, SentencePhoneme


@admin.register(Phoneme)
class PhonemeAdmin(admin.ModelAdmin):
    list_display = ['arpabet', 'symbol', 'ipa', 'type', 'example_word']
    list_filter = ['type']
    search_fields = ['arpabet', 'symbol', 'example_word']
    ordering = ['type', 'arpabet']


class SentencePhonemeInline(admin.TabularInline):
    model = SentencePhoneme
    extra = 1
    autocomplete_fields = ['phoneme']


@admin.register(ReferenceSentence)
class ReferenceSentenceAdmin(admin.ModelAdmin):
    list_display = ['text_preview', 'difficulty_level', 'source', 'is_validated', 'created_at']
    list_filter = ['difficulty_level', 'source', 'is_validated']
    search_fields = ['text']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [SentencePhonemeInline]
    
    def text_preview(self, obj):
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_preview.short_description = 'Text'


@admin.register(SentencePhoneme)
class SentencePhonemeAdmin(admin.ModelAdmin):
    list_display = ['sentence', 'phoneme', 'position', 'word_context']
    list_filter = ['position', 'phoneme']
    search_fields = ['word_context', 'sentence__text']
    autocomplete_fields = ['sentence', 'phoneme']
