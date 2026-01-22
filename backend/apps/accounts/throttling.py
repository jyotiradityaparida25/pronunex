"""
Custom throttle classes for Pronunex authentication endpoints.

Each throttle class has an explicit scope that maps to settings.REST_FRAMEWORK['DEFAULT_THROTTLE_RATES'].
"""

from rest_framework.throttling import AnonRateThrottle, UserRateThrottle


class LoginRateThrottle(AnonRateThrottle):
    """
    Throttle login attempts to prevent brute-force attacks.
    Rate: 5/minute (configurable in settings)
    """
    scope = 'login'


class PasswordResetRateThrottle(AnonRateThrottle):
    """
    Throttle password reset requests to prevent email spam.
    Rate: 3/hour (configurable in settings)
    """
    scope = 'password_reset'


class SignupRateThrottle(AnonRateThrottle):
    """
    Throttle signup attempts to prevent mass account creation.
    Rate: 10/hour (configurable in settings)
    """
    scope = 'signup'


class AuthenticatedUserThrottle(UserRateThrottle):
    """
    Throttle for authenticated user actions.
    Rate: 1000/hour (configurable in settings)
    """
    scope = 'user'
