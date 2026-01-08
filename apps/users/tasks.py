"""
Celery tasks for Users app.
"""
from celery import shared_task
from django.utils import timezone
from .models import APIKey


@shared_task
def check_expired_api_keys():
    """Check and deactivate expired API keys."""
    now = timezone.now()
    
    # Deactivate expired API keys
    expired_keys = APIKey.objects.filter(
        end_date__lt=now,
        is_active=True
    )
    
    for key in expired_keys:
        key.is_active = False
        key.save()
    
    return f"Deactivated {expired_keys.count()} expired API keys"
