"""
Serializers for Billing app.
"""
from rest_framework import serializers
from .models import SubscriptionPlan, Subscription, Payment


class SubscriptionPlanSerializer(serializers.ModelSerializer):
    """Serializer for SubscriptionPlan."""
    
    class Meta:
        model = SubscriptionPlan
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class SubscriptionSerializer(serializers.ModelSerializer):
    """Serializer for Subscription."""
    plan_name = serializers.CharField(source='plan.name', read_only=True)
    plan_type = serializers.CharField(source='plan.plan_type', read_only=True)
    conversion_limit = serializers.IntegerField(source='plan.conversion_limit', read_only=True)
    
    class Meta:
        model = Subscription
        fields = '__all__'
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']


class PaymentSerializer(serializers.ModelSerializer):
    """Serializer for Payment."""
    subscription_plan_name = serializers.CharField(source='subscription.plan.name', read_only=True, allow_null=True)
    
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
    
    def validate_payment_method(self, value):
        """Validate payment method choice."""
        valid_methods = [choice[0] for choice in Payment.PAYMENT_METHODS]
        if value not in valid_methods:
            raise serializers.ValidationError(
                f'Invalid payment method. Must be one of: {", ".join(valid_methods)}'
            )
        return value
