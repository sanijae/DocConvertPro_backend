# Files to Remove After Migration

## Status: Ready for Cleanup

After verifying that all endpoints work correctly with the new structure, you can safely remove these files:

## Old App Files (pdf_app/)

### Can be removed:
- `pdf_app/views.py` - All views migrated to new apps
- `pdf_app/urls.py` - URLs migrated to new apps
- `pdf_app/models.py` - Models migrated to new apps
- `pdf_app/serializer.py` - Serializers migrated to new apps
- `pdf_app/admin.py` - Admin migrated to new apps
- `pdf_app/forms.py` - If not needed
- `pdf_app/authentication.py` - If not needed
- `pdf_app/task.py` - If not needed

### Keep temporarily (for reference):
- `pdf_app/utils.py` - May contain utility functions needed for conversions
- `pdf_app/digital_sign.py` - May contain digital signature logic
- `pdf_app/migrations/` - Keep for database history

## Steps to Remove:

1. **Test all endpoints** to ensure they work:
   ```bash
   # Test user endpoints
   curl http://localhost:8000/api/users/register/
   
   # Test billing endpoints
   curl http://localhost:8000/api/billing/plans/
   
   # Test tools endpoints
   curl http://localhost:8000/api/tools/documents/
   ```

2. **Backup old files** (optional):
   ```bash
   mkdir backup
   cp -r pdf_app backup/
   ```

3. **Remove pdf_app from INSTALLED_APPS** in `config/settings/base.py`

4. **Delete old files**:
   ```bash
   # Windows PowerShell
   Remove-Item -Recurse -Force pdf_app\views.py
   Remove-Item -Recurse -Force pdf_app\urls.py
   Remove-Item -Recurse -Force pdf_app\models.py
   Remove-Item -Recurse -Force pdf_app\serializer.py
   Remove-Item -Recurse -Force pdf_app\admin.py
   ```

5. **Update any remaining imports** that reference `pdf_app`

6. **Run tests** to ensure nothing breaks

## Migration Checklist

- [x] Create new app structure
- [x] Migrate models
- [x] Migrate serializers
- [x] Migrate views structure
- [x] Migrate URLs
- [x] Update settings
- [ ] Migrate actual conversion logic (from pdf_app/views.py functions)
- [ ] Test all endpoints
- [ ] Remove old files
- [ ] Update frontend API calls

## Note

The conversion views in `apps/tools/conversion_views.py` are currently placeholders. 
You need to copy the actual conversion logic from `pdf_app/views.py` functions into these views.
