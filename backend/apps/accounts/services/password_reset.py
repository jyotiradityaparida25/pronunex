"""
Password Reset Service for Pronunex.

Handles token creation, validation, and password reset flow.
Tokens are stored as SHA-256 hashes for security.
"""

import hashlib
import logging
from datetime import timedelta
from typing import Optional, Tuple

from django.conf import settings
from django.utils import timezone

from ..models import User, PasswordResetToken

logger = logging.getLogger(__name__)


class PasswordResetService:
    """
    Service for password reset operations.
    
    Security features:
    - Tokens are hashed before storage (SHA-256)
    - Tokens expire after configurable duration
    - Single-use enforcement
    - No user enumeration (same response for valid/invalid emails)
    """
    
    def __init__(self):
        self.token_expiry_hours = getattr(
            settings, 'AUTH_CONFIG', {}
        ).get('PASSWORD_RESET_TOKEN_EXPIRY_HOURS', 24)
    
    def request_reset(self, email: str) -> Tuple[bool, Optional[str]]:
        """
        Request a password reset for the given email.
        
        Args:
            email: User email address
            
        Returns:
            Tuple of (success, raw_token or None)
            raw_token is returned only if user exists (to send via email)
        """
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # Do not reveal if email exists
            logger.info("Password reset requested for non-existent email")
            return (True, None)
        
        # Invalidate any existing unused tokens for this user
        PasswordResetToken.objects.filter(
            user=user, is_used=False
        ).update(is_used=True)
        
        # Create new token
        expires_at = timezone.now() + timedelta(hours=self.token_expiry_hours)
        raw_token = PasswordResetToken.create_token(user, expires_at)
        
        logger.info("Password reset token created for user")
        
        return (True, raw_token)
    
    def validate_token(self, raw_token: str) -> Optional[PasswordResetToken]:
        """
        Validate a password reset token.
        
        Args:
            raw_token: The raw token received from the user
            
        Returns:
            PasswordResetToken instance if valid, None otherwise
        """
        reset_token = PasswordResetToken.validate_token(raw_token)
        
        if not reset_token:
            logger.warning("Invalid password reset token attempt")
            return None
        
        if reset_token.expires_at < timezone.now():
            logger.warning("Expired password reset token attempt")
            return None
        
        return reset_token
    
    def reset_password(self, raw_token: str, new_password: str) -> Tuple[bool, str]:
        """
        Reset password using a valid token.
        
        Args:
            raw_token: The raw token from the reset link
            new_password: The new password to set
            
        Returns:
            Tuple of (success, message)
        """
        reset_token = self.validate_token(raw_token)
        
        if not reset_token:
            return (False, "Invalid or expired token.")
        
        # Update password
        user = reset_token.user
        user.set_password(new_password)
        user.save()
        
        # Mark token as used
        reset_token.is_used = True
        reset_token.save()
        
        logger.info("Password reset completed successfully")
        
        return (True, "Password has been reset successfully.")
