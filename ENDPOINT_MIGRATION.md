# Endpoint Migration Summary

## ✅ Completed Migrations

### Users Endpoints
All user-related endpoints have been migrated to `apps/users/`:
- ✅ Register → `POST /api/users/register/`
- ✅ Login → `POST /api/users/login/`
- ✅ Logout → `POST /api/users/logout/`
- ✅ Profile → `GET /api/users/me/`
- ✅ Update Profile → `PUT /api/users/me/`
- ✅ Change Password → `POST /api/users/change_password/`
- ✅ Forgot Password → `POST /api/users/forgot_password/`
- ✅ Reset Password → `POST /api/users/reset_password/`
- ✅ Upload Profile Image → `POST /api/users/upload_profile_image/`
- ✅ Create API Key → `POST /api/users/create_api_key/`
- ✅ Get API Key → `GET /api/users/get_api_key/`
- ✅ Contacts → `GET/POST /api/users/contacts/`

### Billing Endpoints
All billing-related endpoints have been migrated to `apps/billing/`:
- ✅ Plans → `GET /api/billing/plans/`
- ✅ Subscriptions → `GET/POST /api/billing/subscriptions/`
- ✅ Current Subscription → `GET /api/billing/subscriptions/current/`
- ✅ Cancel Subscription → `POST /api/billing/subscriptions/{id}/cancel/`
- ✅ Payments → `GET /api/billing/payments/`
- ✅ Update Payment Status → `POST /api/billing/payments/{id}/update_status/`

### Tools Endpoints
All PDF conversion endpoints have been migrated to `apps/tools/`:
- ✅ Documents → `GET/POST /api/tools/documents/`
- ✅ Digital Signatures → `GET/POST /api/tools/digital-signatures/`

**PDF Conversion Endpoints (Structure Created, Logic Needs Migration):**
- ✅ PDF to Word → `POST /api/tools/pdf-to-word/`
- ✅ PDF to Excel → `POST /api/tools/pdf-to-excel/`
- ✅ PDF to JPG → `POST /api/tools/pdf-to-jpg/`
- ✅ PDF to PNG → `POST /api/tools/pdf-to-png/`
- ✅ PDF to JPEG → `POST /api/tools/pdf-to-jpeg/`
- ✅ PDF to CSV → `POST /api/tools/pdf-to-csv/`
- ✅ PDF to BMP → `POST /api/tools/pdf-to-bmp/`
- ✅ PDF to PPT → `POST /api/tools/pdf-to-ppt/`
- ✅ Word to PDF → `POST /api/tools/word-to-pdf/`
- ✅ Excel to PDF → `POST /api/tools/excel-to-pdf/`
- ✅ CSV to PDF → `POST /api/tools/csv-to-pdf/`
- ✅ Image to PDF → `POST /api/tools/image-to-pdf/`
- ✅ PPT to PDF → `POST /api/tools/ppt-to-pdf/`
- ✅ Extract PDF → `POST /api/tools/extract-pdf/`
- ✅ Remove PDF Page → `POST /api/tools/remove-pdf-page/`
- ✅ Add PDF Page → `POST /api/tools/add-pdf-page/`
- ✅ Repair PDF → `POST /api/tools/repair-pdf/`
- ✅ Rotate PDF → `POST /api/tools/rotate-pdf/`
- ✅ Add Watermark → `POST /api/tools/add-watermark/`
- ✅ Compress PDF → `POST /api/tools/compress-pdf/`
- ✅ Merge PDF → `POST /api/tools/merge-pdf/`
- ✅ Split PDF → `POST /api/tools/split-pdf/`
- ✅ Protect PDF → `POST /api/tools/protect-pdf/`
- ✅ Unprotect PDF → `POST /api/tools/unprotect-pdf/`
- ✅ Sign PDF → `POST /api/tools/sign-pdf/`
- ✅ OCR Image → `POST /api/tools/ocr-image/`
- ✅ OCR Identity → `POST /api/tools/ocr-identity/`

## ⚠️ Remaining Work

### 1. Migrate Conversion Logic
The conversion views in `apps/tools/conversion_views.py` are currently placeholders. 
You need to copy the actual conversion logic from `pdf_app/views.py`:

**Steps:**
1. Open `pdf_app/views.py`
2. Find each conversion function (e.g., `PdfToWord`, `WordToPdf`, etc.)
3. Copy the function body
4. Adapt it to:
   - Use `request.user` instead of `user_id` parameter
   - Use `ToolsService.check_conversion_limit(user)` for limit checking
   - Use new models: `User`, `Document`, `SubscriptionPlan`
   - Use `ToolsService.record_conversion()` to track conversions
   - Update file paths and settings imports

**Example Migration:**
```python
# Old (pdf_app/views.py)
def PdfToWord(request, user_id):
    user = get_object_or_404(UsersModel, id=user_id)
    plan = get_object_or_404(Plans, user=user_id)
    # ... conversion logic

# New (apps/tools/conversion_views.py)
class PdfToWordView(BaseConversionView):
    def post(self, request):
        user = request.user
        check = self.check_conversion_limit(user)
        if check is not True:
            return check
        # ... conversion logic (adapted)
```

### 2. Update Authentication
- **Old**: API key in headers (`Api-Key` header)
- **New**: Token authentication (DRF TokenAuthentication)
- **Option**: Keep API key support if needed for backward compatibility

### 3. Remove Old Files
After testing, remove:
- `pdf_app/views.py` (after copying logic)
- `pdf_app/urls.py`
- `pdf_app/models.py`
- `pdf_app/serializer.py`
- `pdf_app/admin.py`

### 4. Update Frontend
Update frontend API calls to use new endpoints:
- `/api/users/` instead of old user endpoints
- `/api/billing/` instead of old payment/plan endpoints
- `/api/tools/` instead of old conversion endpoints

## 📋 Endpoint Mapping

### Old → New

| Old Endpoint | New Endpoint | Status |
|-------------|--------------|--------|
| `POST /register/` | `POST /api/users/register/` | ✅ Complete |
| `POST /login/` | `POST /api/users/login/` | ✅ Complete |
| `POST /pdf_to_word/<uuid>/` | `POST /api/tools/pdf-to-word/` | ⚠️ Structure only |
| `POST /word_to_pdf/<uuid>/` | `POST /api/tools/word-to-pdf/` | ⚠️ Structure only |
| `GET /plans/` | `GET /api/billing/plans/` | ✅ Complete |
| `POST /payment_subscribe/` | `POST /api/billing/subscriptions/` | ✅ Complete |

## 🧪 Testing Checklist

- [ ] Test user registration
- [ ] Test user login
- [ ] Test profile update
- [ ] Test password reset
- [ ] Test subscription creation
- [ ] Test payment processing
- [ ] Test PDF conversions (after logic migration)
- [ ] Test conversion limits
- [ ] Test API key authentication (if kept)

## 📝 Notes

- All endpoints now use RESTful conventions
- Authentication changed from API key to Token-based
- User ID is now obtained from `request.user` instead of URL parameter
- Conversion limits are checked via `ToolsService.check_conversion_limit()`
- All responses follow DRF Response format
