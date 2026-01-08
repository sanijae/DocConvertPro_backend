# Cleanup Plan - Removing Old Files

## Files/Apps to Remove

### 1. Old App: `pdf_app/`
**Status**: Can be removed after migrating PDF conversion logic
- All models migrated to new apps
- Views need to be migrated to `apps/tools/`
- Utils might have reusable code (fonts, etc.)

### 2. Old Config: `config/pdf_office/`
**Status**: Safe to remove
- Replaced by `config/settings/`
- No longer referenced

### 3. Old Templates (if not needed)
- `templates/` - Check if frontend uses these

## Migration Checklist Before Removal

- [ ] Migrate PDF conversion views from `pdf_app/views.py` to `apps/tools/`
- [ ] Copy any useful utilities from `pdf_app/utils/` to `apps/tools/` or `common/`
- [ ] Copy font files if needed for PDF processing
- [ ] Verify no imports reference `pdf_app` or `pdf_office`

## Safe to Remove Now

1. `config/pdf_office/` - Old settings directory
2. `pdf_app/migrations/` - Old migrations (after new migrations are applied)
3. `pdf_app/admin.py` - Replaced by new admin files
4. `pdf_app/models.py` - Replaced by new models
5. `pdf_app/serializer.py` - Replaced by new serializers

## Keep for Now (Need Migration)

1. `pdf_app/views.py` - Contains PDF conversion logic
2. `pdf_app/utils/` - May contain reusable utilities
3. `pdf_app/digital_sign.py` - Digital signature logic
4. `pdf_app/authentication.py` - Check if needed
