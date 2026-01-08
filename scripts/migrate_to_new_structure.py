"""
Script to help migrate from old pdf_app structure to new apps structure.

WARNING: This script will reset the database. Use only in development!
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from django.core.management import call_command
from django.db import connection
from apps.users.models import User
from apps.billing.models import SubscriptionPlan, Subscription, Payment
from apps.tools.models import Document, DigitalSignature

def reset_database():
    """Reset database and create fresh migrations."""
    print("⚠️  WARNING: This will delete all existing data!")
    response = input("Are you sure you want to continue? (yes/no): ")
    if response.lower() != 'yes':
        print("Migration cancelled.")
        return False
    
    print("\n1. Resetting database...")
    call_command('flush', '--noinput')
    
    print("\n2. Removing old migrations...")
    # Delete old migration files if they exist
    old_migration_paths = [
        'pdf_app/migrations',
    ]
    
    print("\n3. Creating new migrations...")
    call_command('makemigrations', 'users')
    call_command('makemigrations', 'billing')
    call_command('makemigrations', 'tools')
    
    print("\n4. Applying migrations...")
    call_command('migrate', '--run-syncdb')
    
    print("\n5. Creating initial data...")
    create_initial_data()
    
    print("\n✅ Migration completed successfully!")
    return True

def create_initial_data():
    """Create initial subscription plans."""
    plans_data = [
        {
            'name': 'Free Plan',
            'plan_type': 'free',
            'conversion_limit': 10,
            'price_monthly': 0.00,
            'price_yearly': 0.00,
            'features': ['10 conversions/month', 'Basic PDF tools', 'Email support']
        },
        {
            'name': 'Basic Plan',
            'plan_type': 'basic',
            'conversion_limit': 100,
            'price_monthly': 9.99,
            'price_yearly': 99.99,
            'features': ['100 conversions/month', 'All PDF tools', 'Priority support']
        },
        {
            'name': 'Premium Plan',
            'plan_type': 'premium',
            'conversion_limit': 500,
            'price_monthly': 19.99,
            'price_yearly': 199.99,
            'features': ['500 conversions/month', 'All PDF tools', 'API access', 'Priority support']
        },
        {
            'name': 'Enterprise Plan',
            'plan_type': 'enterprise',
            'conversion_limit': None,  # Unlimited
            'price_monthly': 49.99,
            'price_yearly': 499.99,
            'features': ['Unlimited conversions', 'All PDF tools', 'API access', 'Dedicated support', 'Custom integrations']
        }
    ]
    
    for plan_data in plans_data:
        SubscriptionPlan.objects.get_or_create(
            name=plan_data['name'],
            defaults=plan_data
        )
        print(f"   ✓ Created {plan_data['name']}")

if __name__ == '__main__':
    reset_database()
