# Migration Guide: Old Structure to New Structure

## Important Notes

⚠️ **WARNING**: Changing `AUTH_USER_MODEL` requires careful migration. The existing database has migrations that depend on the old user model.

## Option 1: Fresh Start (Recommended for Development)

If you're in development and can afford to lose existing data:

1. **Backup your database** (if needed):
   ```bash
   python manage.py dumpdata > backup.json
   ```

2. **Reset the database**:
   ```bash
   python manage.py flush
   ```

3. **Delete old migration files** (optional, to clean up):
   - Remove `pdf_app/migrations/` (keep `__init__.py`)

4. **Create new migrations**:
   ```bash
   python manage.py makemigrations users
   python manage.py makemigrations billing
   python manage.py makemigrations tools
   ```

5. **Apply migrations**:
   ```bash
   python manage.py migrate
   ```

6. **Create initial data** (subscription plans):
   ```bash
   python scripts/migrate_to_new_structure.py
   ```

## Option 2: Data Migration (For Production)

If you need to preserve existing data:

1. **Create a data migration script** to transfer data from old models to new models:
   - `UsersModel` → `apps.users.User`
   - `Plans` → `apps.billing.SubscriptionPlan` and `apps.billing.Subscription`
   - `Payments` → `apps.billing.Payment`
   - `Document` → `apps.tools.Document`
   - `DigitalSignature` → `apps.tools.DigitalSignature`

2. **Steps**:
   ```bash
   # 1. Keep old app temporarily
   # 2. Create new migrations
   python manage.py makemigrations users billing tools
   
   # 3. Fake the initial migration (since we'll migrate data manually)
   python manage.py migrate users 0001 --fake
   python manage.py migrate billing 0001 --fake
   python manage.py migrate tools 0001 --fake
   
   # 4. Run data migration script
   python scripts/migrate_data.py
   
   # 5. Continue with normal migrations
   python manage.py migrate
   ```

## Option 3: Use Migration Script

Run the provided migration script:

```bash
python scripts/migrate_to_new_structure.py
```

This script will:
- Reset the database
- Create all new migrations
- Apply migrations
- Create initial subscription plans

## After Migration

1. **Update admin.py** to register new models:
   ```python
   # apps/users/admin.py
   from django.contrib import admin
   from .models import User, APIKey, Contact
   
   admin.site.register(User)
   admin.site.register(APIKey)
   admin.site.register(Contact)
   ```

2. **Test the API endpoints**:
   - `/api/users/register/`
   - `/api/users/login/`
   - `/api/billing/plans/`

3. **Update frontend** to use new API endpoints

## Common Issues

### Issue: InconsistentMigrationHistory

**Error**: `Migration admin.0001_initial is applied before its dependency users.0001_initial`

**Solution**: Reset the database or use `--fake` flag for initial migrations.

### Issue: AUTH_USER_MODEL conflicts

**Error**: Cannot change AUTH_USER_MODEL after migrations

**Solution**: This requires a fresh database or careful data migration.

## Next Steps

1. ✅ Create migrations for new apps
2. ⏳ Migrate existing data (if needed)
3. ⏳ Update admin registrations
4. ⏳ Refactor PDF conversion views
5. ⏳ Update frontend API calls
6. ⏳ Test all endpoints
