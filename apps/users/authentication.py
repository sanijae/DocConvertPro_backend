"""
API Key Authentication for Users app.
"""
from django.utils import timezone
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import APIKey


class APIKeyAuthentication(BaseAuthentication):
    """Custom authentication using API keys."""
    
    def authenticate(self, request):
        """Authenticate using API key from headers."""
        api_key = request.headers.get('Api-Key') or request.headers.get('X-API-KEY')
        if not api_key:
            return None
        
        try:
            api_key_obj = APIKey.objects.get(key=api_key, is_active=True)
        except APIKey.DoesNotExist:
            raise AuthenticationFailed('Invalid API Key')
        
        # Check if API key is expired
        if api_key_obj.end_date and api_key_obj.end_date < timezone.now().date():
            raise AuthenticationFailed('API Key has expired')
        
        return (api_key_obj.user, None)
