# users/tasks.py
from celery import shared_task
from django.utils import timezone
from .models import APIKey, Plans

@shared_task
def check_expired_keys_and_plans():
    now = timezone.now()

    # Expire API Keys
    expired_keys = APIKey.objects.filter(end_date__lt=now)
    for key in expired_keys:
        key.is_active = False
        key.delete()
        key.save()

    # Expire Plans
    expired_plans = Plans.objects.filter(end_date__lt=now, is_active=True)
    for plan in expired_plans:
        plan.is_active = False
        plan.save()
