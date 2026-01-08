"""
Read-only queries for User app.
"""
from django.db.models import Q
from .models import User, APIKey, Contact


class UserSelector:
    """Selector class for read-only user queries."""
    
    @staticmethod
    def get_user_by_id(user_id):
        """Get user by ID."""
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None
    
    @staticmethod
    def get_user_by_email(email):
        """Get user by email."""
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None
    
    @staticmethod
    def get_active_users():
        """Get all active users."""
        return User.objects.filter(is_active=True)
    
    @staticmethod
    def search_users(query):
        """Search users by email or username."""
        return User.objects.filter(
            Q(email__icontains=query) | Q(username__icontains=query)
        )
    
    @staticmethod
    def get_user_api_key(user):
        """Get API key for user."""
        try:
            return APIKey.objects.get(user=user, is_active=True)
        except APIKey.DoesNotExist:
            return None
    
    @staticmethod
    def get_user_contacts(user):
        """Get all contacts for a user."""
        return Contact.objects.filter(user=user).order_by('-created_at')
