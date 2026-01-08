"""
Admin configuration for Tools app.
"""
from django.contrib import admin
from .models import Document, DigitalSignature


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    """Admin interface for Document model."""
    list_display = ['id', 'user', 'file_type', 'conversion_type', 'uploaded_at']
    list_filter = ['file_type', 'conversion_type', 'uploaded_at']
    search_fields = ['user__email', 'file_type', 'conversion_type']
    readonly_fields = ['uploaded_at']
    date_hierarchy = 'uploaded_at'


@admin.register(DigitalSignature)
class DigitalSignatureAdmin(admin.ModelAdmin):
    """Admin interface for DigitalSignature model."""
    list_display = ['name', 'user', 'date_created']
    list_filter = ['date_created']
    search_fields = ['name', 'user__email']
    readonly_fields = ['date_created']
    date_hierarchy = 'date_created'
