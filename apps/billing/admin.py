"""
Admin configuration for Billing app.
"""
from django.contrib import admin
from .models import SubscriptionPlan, Subscription, Payment


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    """Admin interface for SubscriptionPlan model."""
    list_display = ['name', 'plan_type', 'conversion_limit', 'price_monthly', 'price_yearly', 'is_active', 'created_at']
    list_filter = ['plan_type', 'is_active', 'created_at']
    search_fields = ['name']
    ordering = ['price_monthly']


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """Admin interface for Subscription model."""
    list_display = ['user', 'plan', 'status', 'start_date', 'end_date', 'auto_renew', 'created_at']
    list_filter = ['status', 'auto_renew', 'created_at']
    search_fields = ['user__email', 'plan__name']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """Admin interface for Payment model."""
    list_display = ['user', 'subscription', 'amount', 'currency', 'payment_method', 'status', 'transaction_id', 'created_at']
    list_filter = ['status', 'payment_method', 'created_at']
    search_fields = ['user__email', 'transaction_id', 'ref_code']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
