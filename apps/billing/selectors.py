"""
Read-only queries for Billing app.
"""
from .models import SubscriptionPlan, Subscription, Payment
from django.contrib.auth import get_user_model

User = get_user_model()


class BillingSelector:
    """Selector class for read-only billing queries."""
    
    @staticmethod
    def get_active_plans():
        """Get all active subscription plans."""
        return SubscriptionPlan.objects.filter(is_active=True).order_by('price_monthly')
    
    @staticmethod
    def get_user_subscription(user):
        """Get user's active subscription."""
        return Subscription.objects.filter(
            user=user,
            status='active'
        ).first()
    
    @staticmethod
    def get_user_payments(user):
        """Get all user payments."""
        return Payment.objects.filter(user=user).order_by('-created_at')
    
    @staticmethod
    def get_plan_by_id(plan_id):
        """Get plan by ID."""
        try:
            return SubscriptionPlan.objects.get(id=plan_id, is_active=True)
        except SubscriptionPlan.DoesNotExist:
            return None
