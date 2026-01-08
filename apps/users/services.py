"""
Business logic for User app.
"""
import secrets
from django.db import transaction
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from .models import User, APIKey, PasswordResetToken


class UserService:
    """Service class for user-related business logic."""
    
    @staticmethod
    @transaction.atomic
    def create_user(email, username=None, password=None, **extra_fields):
        """Create a new user."""
        # Generate username from email if not provided
        if not username:
            # Use email prefix as username, append numbers if needed for uniqueness
            base_username = email.split('@')[0].replace('.', '_').replace('+', '_')[:140]
            username = base_username
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{base_username}_{counter}"[:140]
                counter += 1
        
        user = User.objects.create_user(
            email=email,
            username=username,
            password=password,
            **extra_fields
        )
        return user
    
    @staticmethod
    def increment_conversion_count(user):
        """Increment user's conversion count."""
        user.conversion_count += 1
        user.save(update_fields=['conversion_count'])
        return user
    
    @staticmethod
    def increment_file_count(user):
        """Increment user's total file count."""
        user.total_files += 1
        user.save(update_fields=['total_files'])
        return user
    
    @staticmethod
    @transaction.atomic
    def create_api_key(user):
        """Create or get API key for user."""
        api_key, created = APIKey.objects.get_or_create(
            user=user,
            defaults={'key': secrets.token_urlsafe(32)}
        )
        if not created:
            # Regenerate key if it exists
            api_key.key = secrets.token_urlsafe(32)
            api_key.is_active = True
            api_key.save(update_fields=['key', 'is_active'])
        return api_key
    
    @staticmethod
    @transaction.atomic
    def create_password_reset_token(user):
        """Create a password reset token for user."""
        # Invalidate any existing tokens
        PasswordResetToken.objects.filter(user=user, is_used=False).update(is_used=True)
        
        # Create new token
        reset_token = PasswordResetToken.objects.create(user=user)
        return reset_token
    
    @staticmethod
    def send_password_reset_email(user, reset_token):
        """Send password reset email."""
        try:
            reset_url = f"{settings.BASE_HOST_URL}reset-password?token={reset_token.token}"
            subject = 'Password Reset Request'
            message = f"""
            Hello {user.name or user.username},
            
            You requested a password reset. Please click the link below to reset your password:
            {reset_url}
            
            This link will expire in 24 hours.
            
            If you didn't request this, please ignore this email.
            """
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )
            return True
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
