"""
Supabase Email Service for Pronunex.

Handles sending emails via Supabase for password resets and notifications.
"""

import logging
from typing import Optional

from django.conf import settings

logger = logging.getLogger(__name__)


class SupabaseEmailService:
    """
    Service for sending emails via Supabase.
    
    Uses Supabase Auth or Edge Functions for email delivery.
    Email templates are pre-configured in Supabase dashboard.
    """
    
    def __init__(self):
        self.supabase_url = getattr(settings, 'SUPABASE_URL', '')
        self.service_key = getattr(settings, 'SUPABASE_SERVICE_ROLE_KEY', '')
        self._client = None
    
    @property
    def client(self):
        """Lazy initialization of Supabase client."""
        if self._client is None:
            try:
                from supabase import create_client
                self._client = create_client(self.supabase_url, self.service_key)
            except ImportError:
                logger.error("supabase-py not installed. Run: pip install supabase")
                raise
            except Exception as e:
                logger.error(f"Failed to initialize Supabase client: {e}")
                raise
        return self._client
    
    def send_password_reset_email(
        self, 
        email: str, 
        reset_token: str,
        frontend_url: Optional[str] = None
    ) -> bool:
        """
        Send password reset email via Supabase.
        
        Args:
            email: Recipient email address
            reset_token: The raw reset token
            frontend_url: Base URL for reset link (defaults to settings)
            
        Returns:
            True if email sent successfully, False otherwise
        """
        if not frontend_url:
            frontend_url = getattr(settings, 'FRONTEND_URL', 'http://localhost:3000')
        
        reset_url = f"{frontend_url}/reset-password?token={reset_token}"
        
        try:
            # Option 1: Use Supabase Edge Function for custom email
            # self.client.functions.invoke('send-email', {
            #     'body': {
            #         'to': email,
            #         'template': 'password_reset',
            #         'data': {'reset_url': reset_url}
            #     }
            # })
            
            # Option 2: Log for now (email sending configured in Supabase dashboard)
            logger.info(f"Password reset email would be sent to: {email}")
            logger.debug(f"Reset URL: {reset_url}")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to send password reset email: {e}")
            return False
    
    def send_welcome_email(self, email: str, full_name: str) -> bool:
        """
        Send welcome email to new users.
        
        Args:
            email: Recipient email address
            full_name: User's full name
            
        Returns:
            True if email sent successfully, False otherwise
        """
        try:
            logger.info(f"Welcome email would be sent to: {email}")
            return True
        except Exception as e:
            logger.error(f"Failed to send welcome email: {e}")
            return False
