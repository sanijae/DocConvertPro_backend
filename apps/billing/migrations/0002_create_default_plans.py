# Data migration to create default subscription plans

from django.db import migrations
from decimal import Decimal


def create_default_plans(apps, schema_editor):
    """Create default subscription plans."""
    SubscriptionPlan = apps.get_model('billing', 'SubscriptionPlan')
    
    # Free Tier
    SubscriptionPlan.objects.get_or_create(
        plan_type='free',
        defaults={
            'name': 'Free Tier',
            'daily_conversion_limit': 3,
            'file_size_limit_mb': 5,
            'price_monthly': Decimal('0.00'),
            'price_yearly': Decimal('0.00'),
            'currency': 'NGN',
            'watermark': True,
            'batch_conversions': False,
            'ocr_support': False,
            'priority_processing': False,
            'cloud_storage': False,
            'supported_formats': ['pdf', 'jpg', 'jpeg', 'png'],
            'features': [
                'Limited conversions per day (3 files)',
                'File size limit (5MB)',
                'Basic formats only (PDF ↔ images(jpg,png,...), Images ↔ PDF)',
                'Watermark on output'
            ],
            'is_active': True
        }
    )
    
    # Starter Plan
    SubscriptionPlan.objects.get_or_create(
        plan_type='starter',
        defaults={
            'name': 'Starter',
            'daily_conversion_limit': None,  # Unlimited
            'file_size_limit_mb': 100,
            'price_monthly': Decimal('5000.00'),
            'price_yearly': Decimal('60000.00'),  # 12 months (5000 * 12)
            'currency': 'NGN',
            'watermark': False,
            'batch_conversions': False,
            'ocr_support': False,
            'priority_processing': False,
            'cloud_storage': False,
            'supported_formats': ['pdf', 'jpg', 'jpeg', 'png', 'docx', 'doc', 'xlsx', 'xls', 'pptx', 'ppt'],
            'features': [
                'All conversion tools',
                'Unlimited conversions',
                'Larger file size (<100MB)',
                'No watermark'
            ],
            'is_active': True
        }
    )
    
    # Pro Plan
    SubscriptionPlan.objects.get_or_create(
        plan_type='pro',
        defaults={
            'name': 'Pro',
            'daily_conversion_limit': None,  # Unlimited
            'file_size_limit_mb': None,  # Unlimited
            'price_monthly': Decimal('20000.00'),
            'price_yearly': Decimal('240000.00'),  # 12 months (20000 * 12)
            'currency': 'NGN',
            'watermark': False,
            'batch_conversions': True,
            'ocr_support': True,
            'priority_processing': True,
            'cloud_storage': True,
            'supported_formats': ['pdf', 'jpg', 'jpeg', 'png', 'docx', 'doc', 'xlsx', 'xls', 'pptx', 'ppt', 'txt', 'rtf', 'odt', 'ods', 'odp'],
            'features': [
                'Batch conversions',
                'Advanced formats (OCR)',
                'Priority processing',
                'Cloud storage integration',
                'Unlimited conversions',
                'Unlimited file size',
                'No watermark'
            ],
            'is_active': True
        }
    )


def reverse_create_default_plans(apps, schema_editor):
    """Remove default subscription plans."""
    SubscriptionPlan = apps.get_model('billing', 'SubscriptionPlan')
    SubscriptionPlan.objects.filter(plan_type__in=['free', 'starter', 'pro']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_default_plans, reverse_create_default_plans),
    ]
