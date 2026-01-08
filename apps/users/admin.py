"""
Admin configuration for Users app.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, APIKey, Contact, PasswordResetToken


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin interface for User model."""
    list_display = ['email', 'username', 'first_name', 'last_name', 'email_verified', 'conversion_count', 'total_files', 'role', 'is_active', 'date_joined']
    list_filter = ['is_active', 'is_staff', 'email_verified', 'role', 'date_joined']
    search_fields = ['email', 'username', 'first_name', 'last_name']
    ordering = ['-date_joined']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('email_verified', 'conversion_count', 'total_files', 'role', 'profile_image')
        }),
    )


@admin.register(APIKey)
class APIKeyAdmin(admin.ModelAdmin):
    """Admin interface for APIKey model."""
    list_display = ['user', 'key', 'is_active', 'end_date', 'date_created']
    list_filter = ['is_active', 'date_created']
    search_fields = ['user__email', 'key']
    readonly_fields = ['key', 'date_created']


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """Admin interface for Contact model."""
    list_display = ['name', 'email', 'title', 'user', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'email', 'title', 'message']
    readonly_fields = ['created_at']


@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    """Admin interface for PasswordResetToken model."""
    list_display = ['user', 'token', 'is_used', 'created_at', 'expires_at']
    list_filter = ['is_used', 'created_at']
    search_fields = ['user__email', 'token']
    readonly_fields = ['token', 'created_at', 'expires_at']
