"""
API Views for authentication and user management.
"""

from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from django.utils import timezone
from datetime import timedelta
import logging

from .models import User, PasswordResetToken
from .serializers import (
    SignupSerializer,
    LoginSerializer,
    UserProfileSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
    ChangePasswordSerializer,
)

logger = logging.getLogger(__name__)


class SignupView(generics.CreateAPIView):
    """
    POST /api/v1/auth/signup/
    
    Register a new user account.
    """
    
    queryset = User.objects.all()
    serializer_class = SignupSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generate tokens for immediate login
        refresh = RefreshToken.for_user(user)
        
        logger.info(f"New user registered: {user.email}")
        
        return Response({
            'message': 'Registration successful.',
            'user': UserProfileSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    """
    POST /api/v1/auth/login/
    
    Authenticate user and return JWT tokens.
    """
    
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']
        tokens = serializer.get_tokens(user)
        
        logger.info(f"User logged in: {user.email}")
        
        return Response({
            'message': 'Login successful.',
            'user': UserProfileSerializer(user).data,
            'tokens': tokens,
        }, status=status.HTTP_200_OK)


class LogoutView(APIView):
    """
    POST /api/v1/auth/logout/
    
    Blacklist the refresh token to logout user.
    Allows unauthenticated requests to handle expired tokens gracefully.
    """
    
    permission_classes = [AllowAny]
    
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            
            if hasattr(request, 'user') and request.user.is_authenticated:
                logger.info(f"User logged out: {request.user.email}")
            else:
                logger.info("Logout request processed (no authenticated user)")
            
            return Response({
                'message': 'Logout successful.'
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Logout error: {str(e)}")
            # Still return success - client should clear tokens regardless
            return Response({
                'message': 'Logout processed.'
            }, status=status.HTTP_200_OK)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    GET /api/v1/auth/profile/
    PUT /api/v1/auth/profile/
    
    Retrieve or update user profile.
    """
    
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user


class PasswordResetRequestView(APIView):
    """
    POST /api/v1/auth/password/reset/
    
    Request a password reset email.
    """
    
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        
        try:
            user = User.objects.get(email=email)
            
            # Generate reset token
            token = PasswordResetToken.generate_token()
            expires_at = timezone.now() + timedelta(hours=24)
            
            PasswordResetToken.objects.create(
                user=user,
                token=token,
                expires_at=expires_at
            )
            
            # TODO: Send email with reset link
            # For now, log the token (development only)
            logger.info(f"Password reset token for {email}: {token}")
            
        except User.DoesNotExist:
            # Do not reveal if email exists
            pass
        
        return Response({
            'message': 'If the email exists, a reset link has been sent.'
        }, status=status.HTTP_200_OK)


class PasswordResetConfirmView(APIView):
    """
    POST /api/v1/auth/password/reset/confirm/
    
    Confirm password reset with token.
    """
    
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        reset_token = serializer.validated_data['reset_token']
        new_password = serializer.validated_data['new_password']
        
        # Update password
        user = reset_token.user
        user.set_password(new_password)
        user.save()
        
        # Mark token as used
        reset_token.is_used = True
        reset_token.save()
        
        logger.info(f"Password reset completed for: {user.email}")
        
        return Response({
            'message': 'Password has been reset successfully.'
        }, status=status.HTTP_200_OK)


class ChangePasswordView(APIView):
    """
    POST /api/v1/auth/password/change/
    
    Change password while logged in.
    """
    
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        current_password = serializer.validated_data['current_password']
        new_password = serializer.validated_data['new_password']
        
        if not user.check_password(current_password):
            return Response({
                'error': 'Current password is incorrect.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(new_password)
        user.save()
        
        logger.info(f"Password changed for: {user.email}")
        
        return Response({
            'message': 'Password changed successfully.'
        }, status=status.HTTP_200_OK)
