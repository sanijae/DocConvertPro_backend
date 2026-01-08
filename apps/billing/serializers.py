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
    daily_conversion_limit = serializers.IntegerField(source='plan.daily_conversion_limit', read_only=True, allow_null=True)
    file_size_limit_mb = serializers.IntegerField(source='plan.file_size_limit_mb', read_only=True, allow_null=True)
    watermark = serializers.BooleanField(source='plan.watermark', read_only=True)
    batch_conversions = serializers.BooleanField(source='plan.batch_conversions', read_only=True)
    ocr_support = serializers.BooleanField(source='plan.ocr_support', read_only=True)
    priority_processing = serializers.BooleanField(source='plan.priority_processing', read_only=True)
    cloud_storage = serializers.BooleanField(source='plan.cloud_storage', read_only=True)
    supported_formats = serializers.ListField(source='plan.supported_formats', read_only=True)
    
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
