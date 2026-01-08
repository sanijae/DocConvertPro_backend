"""
Business logic for Tools app.
"""
from django.db import transaction
from django.contrib.auth import get_user_model
from .models import Document, DigitalSignature
from apps.billing.selectors import BillingSelector
from apps.users.services import UserService
from common.exceptions import ConversionLimitExceeded, SubscriptionRequired

User = get_user_model()


class ToolsService:
    """Service class for tools-related business logic."""
    
    @staticmethod
    def check_conversion_limit(user):
        """Check if user can perform conversion based on their plan."""
        subscription = BillingSelector.get_user_subscription(user)
        
        if not subscription:
            # No subscription, assign free plan
            from apps.billing.services import BillingService
            subscription = BillingService.assign_free_plan(user)
        
        if not subscription:
            raise SubscriptionRequired("No active subscription found.")
        
        plan = subscription.plan
        
        # If conversion_limit is None, unlimited conversions
        if plan.conversion_limit is None:
            return True
        
        # Check if user has exceeded limit
        if user.conversion_count >= plan.conversion_limit:
            raise ConversionLimitExceeded(
                f"You have reached your conversion limit of {plan.conversion_limit} for your {plan.name} plan."
            )
        
        return True
    
    @staticmethod
    @transaction.atomic
    def record_conversion(user, file_type, conversion_type):
        """Record a conversion for the user."""
        # Check conversion limit
        ToolsService.check_conversion_limit(user)
        
        # Increment conversion count
        UserService.increment_conversion_count(user)
        UserService.increment_file_count(user)
        
        # Create document record
        document = Document.objects.create(
            user=user,
            file_type=file_type,
            conversion_type=conversion_type
        )
        
        return document
    
    @staticmethod
    def create_document(user, file, file_type, conversion_type, converted_file_url=None):
        """Create a document record."""
        document = Document.objects.create(
            user=user,
            file=file,
            file_type=file_type,
            conversion_type=conversion_type,
            converted_file_url=converted_file_url
        )
        return document
    
    @staticmethod
    def create_digital_signature(user, name, file, signed_file_url=None, signature=None):
        """Create a digital signature record."""
        digital_signature = DigitalSignature.objects.create(
            user=user,
            name=name,
            file=file,
            signed_file_url=signed_file_url,
            signature=signature
        )
        return digital_signature
