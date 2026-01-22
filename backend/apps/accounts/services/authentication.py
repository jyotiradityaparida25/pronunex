"""
Authentication Service for Pronunex.

Handles login, logout, and token management logic.
"""

import logging
from typing import Dict, Optional, Tuple

from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from ..models import User

logger = logging.getLogger(__name__)


class AuthenticationService:
    """
    Service for authentication operations.
    
    Centralizes login/logout logic for cleaner views.
    """
    
    def login(self, email: str, password: str) -> Tuple[bool, Optional[User], Optional[Dict], str]:
        """
        Authenticate user and generate JWT tokens.
        
        Args:
            email: User email
            password: User password
            
        Returns:
            Tuple of (success, user, tokens, message)
        """
        user = authenticate(username=email, password=password)
        
        if not user:
            logger.warning(f"Failed login attempt for email: {email}")
            return (False, None, None, "Invalid email or password.")
        
        if not user.is_active:
            logger.warning(f"Login attempt for disabled account: {email}")
            return (False, None, None, "User account is disabled.")
        
        tokens = self.generate_tokens(user)
        logger.info(f"User logged in: {user.email}")
        
        return (True, user, tokens, "Login successful.")
    
    def generate_tokens(self, user: User) -> Dict[str, str]:
        """
        Generate JWT tokens for a user.
        
        Args:
            user: User instance
            
        Returns:
            Dict with 'refresh' and 'access' tokens
        """
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
    
    def logout(self, refresh_token: Optional[str]) -> Tuple[bool, str]:
        """
        Blacklist the refresh token to logout user.
        
        Args:
            refresh_token: The refresh token to blacklist
            
        Returns:
            Tuple of (success, message)
        """
        if not refresh_token:
            return (True, "Logout processed.")
        
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            logger.info("User logged out successfully")
            return (True, "Logout successful.")
        except Exception as e:
            logger.error(f"Logout error: {str(e)}")
            # Still return success - client should clear tokens
            return (True, "Logout processed.")
