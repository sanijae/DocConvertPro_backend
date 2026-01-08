"""
Business logic for Billing app.
"""
from django.db import transaction
from django.utils import timezone
from datetime import timedelta
from .models import SubscriptionPlan, Subscription, Payment


class BillingService:
    """Service class for billing-related business logic."""
    
    @staticmethod
    @transaction.atomic
    def create_subscription(user, plan, payment_method='paystack', billing_cycle='monthly'):
        """
        Create a new subscription and associated payment record.
        
        Args:
            user: User instance
            plan: SubscriptionPlan instance
            payment_method: Payment method (stripe, paypal, paystack)
            billing_cycle: Billing cycle ('monthly' or 'yearly')
        
        Returns:
            tuple: (subscription, payment) instances
        """
        # Validate payment method
        valid_methods = [choice[0] for choice in Payment.PAYMENT_METHODS]
        if payment_method not in valid_methods:
            raise ValueError(f'Invalid payment method. Must be one of: {", ".join(valid_methods)}')
        
        # Validate billing cycle
        valid_cycles = ['monthly', 'yearly']
        if billing_cycle not in valid_cycles:
            raise ValueError(f'Invalid billing cycle. Must be one of: {", ".join(valid_cycles)}')
        
        # Calculate end date based on billing cycle
        start_date = timezone.now()
        
        if billing_cycle == 'yearly':
            end_date = start_date + timedelta(days=365)
            payment_amount = plan.price_yearly
        else:
            end_date = start_date + timedelta(days=30)
            payment_amount = plan.price_monthly
        
        # Cancel any existing active subscriptions
        Subscription.objects.filter(
            user=user,
            status='active'
        ).update(status='cancelled', auto_renew=False)
        
        subscription = Subscription.objects.create(
            user=user,
            plan=plan,
            start_date=start_date,
            end_date=end_date,
            status='pending'
        )
        
        # Create payment record
        payment = Payment.objects.create(
            user=user,
            subscription=subscription,
            amount=payment_amount,
            payment_method=payment_method,
            status='pending'
        )
        
        return subscription, payment
    
    @staticmethod
    @transaction.atomic
    def activate_subscription(subscription):
        """Activate a subscription."""
        subscription.status = 'active'
        subscription.save(update_fields=['status'])
        return subscription
    
    @staticmethod
    def get_free_plan():
        """Get the free subscription plan."""
        return SubscriptionPlan.objects.filter(plan_type='free', is_active=True).first()
    
    @staticmethod
    @transaction.atomic
    def assign_free_plan(user):
        """Assign free plan to a user."""
        free_plan = BillingService.get_free_plan()
        if not free_plan:
            return None
        
        # Cancel any existing active subscriptions (except free plan)
        Subscription.objects.filter(
            user=user,
            status='active'
        ).exclude(plan=free_plan).update(status='cancelled', auto_renew=False)
        
        # Get or create free plan subscription
        subscription, created = Subscription.objects.get_or_create(
            user=user,
            plan=free_plan,
            defaults={
                'status': 'active',
                'start_date': timezone.now(),
                'end_date': None,
                'auto_renew': False
            }
        )
        
        if not created:
            subscription.status = 'active'
            subscription.start_date = timezone.now()
            subscription.end_date = None
            subscription.auto_renew = False
            subscription.save(update_fields=['status', 'start_date', 'end_date', 'auto_renew'])
        
        return subscription
    
    @staticmethod
    @transaction.atomic
    def cancel_subscription(subscription):
        """Cancel a subscription and revert to free plan."""
        subscription.status = 'cancelled'
        subscription.auto_renew = False
        subscription.save(update_fields=['status', 'auto_renew'])
        
        # Revert user to free plan
        BillingService.assign_free_plan(subscription.user)
        
        return subscription
    
    @staticmethod
    @transaction.atomic
    def update_payment_status(payment, status, transaction_id=None):
        """
        Update payment status and optionally set transaction_id.
        
        Args:
            payment: Payment instance
            status: New payment status (pending, completed, failed, refunded)
            transaction_id: Optional transaction ID from payment gateway
        
        Returns:
            Updated Payment instance
        """
        valid_statuses = [choice[0] for choice in Payment.STATUS_CHOICES]
        if status not in valid_statuses:
            raise ValueError(f'Invalid status. Must be one of: {", ".join(valid_statuses)}')
        
        payment.status = status
        if transaction_id:
            payment.transaction_id = transaction_id
        payment.save(update_fields=['status', 'transaction_id'] if transaction_id else ['status'])
        
        # If payment is completed, activate the subscription
        if status == 'completed' and payment.subscription:
            if payment.subscription.status == 'pending':
                BillingService.activate_subscription(payment.subscription)
        
        return payment
    
    @staticmethod
    def get_payment_by_transaction_id(transaction_id):
        """Get payment by transaction ID."""
        try:
            return Payment.objects.get(transaction_id=transaction_id)
        except Payment.DoesNotExist:
            return None
