"""
User models for authentication and user profiles.
"""
import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from datetime import timedelta


class User(AbstractUser):
    """Custom User model."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(
        max_length=150,
        unique=True,
        null=True,
        blank=True,
        validators=[AbstractUser.username_validator],
        help_text='Optional. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'
    )
    email = models.EmailField(unique=True)
    email_verified = models.BooleanField(default=False)
    conversion_count = models.IntegerField(default=0)
    total_files = models.IntegerField(default=0)
    role = models.CharField(max_length=100, default='user')
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    class Meta:
        app_label = 'users'
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return self.email


class PasswordResetToken(models.Model):
    """Token for password reset functionality."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='password_reset_tokens')
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    
    class Meta:
        app_label = 'users'
        db_table = 'password_reset_tokens'
        verbose_name = 'Password Reset Token'
        verbose_name_plural = 'Password Reset Tokens'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Password reset token for {self.user.email}"
    
    def save(self, *args, **kwargs):
        """Set expiration time if not provided."""
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(hours=24)  # 24 hour expiration
        super().save(*args, **kwargs)
    
    def is_valid(self):
        """Check if token is valid (not expired and not used)."""
        return not self.is_used and self.expires_at > timezone.now()
    
    def mark_as_used(self):
        """Mark token as used."""
        self.is_used = True
        self.save(update_fields=['is_used'])


class APIKey(models.Model):
    """API Key model for user API access."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    key = models.CharField(max_length=200, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='api_key')
    end_date = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        app_label = 'users'
        db_table = 'api_keys'
        verbose_name = 'API Key'
        verbose_name_plural = 'API Keys'
    
    def __str__(self):
        return f"API Key for {self.user.email}"


class Contact(models.Model):
    """Contact model for user inquiries."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    title = models.CharField(max_length=200, default='')
    message = models.TextField(default='')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contacts', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        app_label = 'users'
        db_table = 'contacts'
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.email}"
