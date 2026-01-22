from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, PasswordResetToken


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'full_name', 'proficiency_level', 'is_active', 'created_at']
    list_filter = ['proficiency_level', 'is_active', 'is_email_verified']
    search_fields = ['email', 'full_name', 'username']
    ordering = ['-created_at']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Profile', {
            'fields': ('full_name', 'native_language', 'proficiency_level', 'is_email_verified')
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Profile', {
            'fields': ('email', 'full_name', 'native_language', 'proficiency_level')
        }),
    )


@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    """
    Admin for password reset tokens.
    Token hash is intentionally not displayed (principle of least privilege).
    """
    list_display = ['user', 'created_at', 'expires_at', 'is_used']
    list_filter = ['is_used', 'created_at']
    search_fields = ['user__email']
    ordering = ['-created_at']
    # No token_hash field exposed - admins do not need access to reset tokens
