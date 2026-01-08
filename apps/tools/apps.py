"""
Tools app configuration.
"""
from django.apps import AppConfig


class ToolsConfig(AppConfig):
    """Tools app configuration."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.tools'
    verbose_name = 'Tools'
