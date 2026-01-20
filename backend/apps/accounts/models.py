"""
Custom User Model for Pronunex.

Implements email-based authentication with proficiency tracking.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models
import secrets


class User(AbstractUser):
    """
    Custom user model with email-based authentication.
    Tracks native language and proficiency level for adaptive exercises.
    """
    
    PROFICIENCY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100)
    native_language = models.CharField(max_length=50, blank=True)
    proficiency_level = models.CharField(
        max_length=20, 
        choices=PROFICIENCY_CHOICES, 
        default='beginner'
    )
    is_email_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'full_name']
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.email


class PasswordResetToken(models.Model):
    """
    Token model for password reset functionality.
    Tokens expire after a configurable duration.
    """
    
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='reset_tokens'
    )
    token = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Password Reset Token'
        verbose_name_plural = 'Password Reset Tokens'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Reset token for {self.user.email}"
    
    @classmethod
    def generate_token(cls):
        """Generate a cryptographically secure token."""
        return secrets.token_urlsafe(48)
