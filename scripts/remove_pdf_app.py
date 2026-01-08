"""
Script to remove pdf_app directory after migration is complete.
"""
import os
import shutil
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
PDF_APP_DIR = BASE_DIR / 'pdf_app'

def remove_pdf_app():
    """Remove pdf_app directory."""
    if not PDF_APP_DIR.exists():
        print("✅ pdf_app directory does not exist. Already removed.")
        return
    
    print("⚠️  WARNING: This will permanently delete the pdf_app directory!")
    print(f"Location: {PDF_APP_DIR}")
    response = input("Are you sure you want to continue? (yes/no): ")
    
    if response.lower() != 'yes':
        print("❌ Removal cancelled.")
        return
    
    try:
        # Keep migrations for reference (optional)
        keep_migrations = input("Keep migrations directory for reference? (yes/no): ")
        if keep_migrations.lower() == 'yes':
            migrations_backup = BASE_DIR / 'backup_migrations'
            if PDF_APP_DIR / 'migrations' exists():
                shutil.copytree(PDF_APP_DIR / 'migrations', migrations_backup / 'pdf_app_migrations')
                print(f"✅ Migrations backed up to {migrations_backup}")
        
        # Remove pdf_app directory
        shutil.rmtree(PDF_APP_DIR)
        print("✅ pdf_app directory removed successfully!")
        print("\n📝 Next steps:")
        print("1. Run: python manage.py makemigrations")
        print("2. Run: python manage.py migrate")
        print("3. Test all endpoints")
        
    except Exception as e:
        print(f"❌ Error removing pdf_app: {e}")

if __name__ == '__main__':
    remove_pdf_app()
