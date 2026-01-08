"""
Admin configuration for Billing app.
"""
from django.contrib import admin
from .models import SubscriptionPlan, Subscription, Payment


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    """Admin interface for SubscriptionPlan model."""
    list_display = ['name', 'plan_type', 'daily_conversion_limit', 'file_size_limit_mb', 'price_monthly', 'currency', 'watermark', 'is_active', 'created_at']
    list_filter = ['plan_type', 'is_active', 'watermark', 'batch_conversions', 'ocr_support', 'created_at']
    search_fields = ['name', 'plan_type']
    ordering = ['price_monthly']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'plan_type', 'is_active')
        }),
        ('Pricing', {
            'fields': ('price_monthly', 'price_yearly', 'currency')
        }),
        ('Limits', {
            'fields': ('daily_conversion_limit', 'file_size_limit_mb')
        }),
        ('Features', {
            'fields': ('watermark', 'batch_conversions', 'ocr_support', 'priority_processing', 'cloud_storage')
        }),
        ('Formats & Features List', {
            'fields': ('supported_formats', 'features')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['created_at', 'updated_at']


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
