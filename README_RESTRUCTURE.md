# Backend Restructure Summary

## Overview
The backend has been restructured to follow modern Django architecture patterns, similar to the stash-backend app structure.

## New Structure

```
DocConvertPro_backend/
├── apps/
│   ├── users/          # User authentication and management
│   ├── tools/          # PDF conversion tools
│   └── billing/        # Subscriptions and payments
├── common/             # Shared utilities
│   ├── exceptions.py
│   ├── utils.py
│   ├── paginations.py
│   └── permissions.py
├── config/             # Project configuration
│   ├── settings/
│   │   ├── base.py
│   │   ├── development.py
│   │   └── production.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
└── middleware/         # Custom middleware (optional)
```

## Key Changes

### 1. Apps Structure
Each app now follows a consistent structure:
- `models.py` - Database models
- `serializers.py` - DRF serializers
- `services.py` - Business logic
- `views.py` - API views
- `urls.py` - URL routing
- `selectors.py` - Read-only queries (where applicable)
- `apps.py` - App configuration

### 2. Users App (`apps/users`)
- Custom User model extending AbstractUser
- Authentication endpoints (register, login, logout)
- Password reset functionality
- API key management
- Contact form handling

### 3. Billing App (`apps/billing`)
- SubscriptionPlan model
- Subscription model with status tracking
- Payment model supporting multiple payment methods (Stripe, PayPal, Paystack)
- Subscription lifecycle management
- Payment status updates

### 4. Tools App (`apps/tools`)
- Document model for file tracking
- DigitalSignature model
- Conversion limit checking based on subscription
- Service layer for conversion logic

### 5. Common Utilities
- Custom exceptions (StorageLimitExceeded, ConversionLimitExceeded, etc.)
- Utility functions (file handling, formatting)
- Custom pagination classes
- Custom permission classes

### 6. Settings
- Split into base, development, and production
- Environment-based configuration
- Better security defaults for production

## Migration Notes

### Next Steps:
1. **Create migrations** for the new models:
   ```bash
   python manage.py makemigrations users
   python manage.py makemigrations billing
   python manage.py makemigrations tools
   ```

2. **Data Migration**: The old `pdf_app` models need to be migrated to the new structure:
   - `UsersModel` → `apps.users.User`
   - `Plans` → `apps.billing.SubscriptionPlan`
   - `Payments` → `apps.billing.Payment`
   - `Document` → `apps.tools.Document`
   - `DigitalSignature` → `apps.tools.DigitalSignature`

3. **Update AUTH_USER_MODEL**: Already set to `apps.users.User`

4. **Migrate PDF conversion views**: The conversion logic from `pdf_app/views.py` needs to be refactored and moved to `apps/tools/views.py` or service methods.

5. **Update frontend API calls**: Update frontend to use new API endpoints:
   - `/api/users/` instead of old user endpoints
   - `/api/billing/` instead of old payment/plan endpoints
   - `/api/tools/` for document conversions

## API Endpoints

### Users
- `POST /api/users/register/` - Register new user
- `POST /api/users/login/` - Login
- `POST /api/users/logout/` - Logout
- `GET /api/users/me/` - Get current user
- `PUT /api/users/me/` - Update profile
- `POST /api/users/forgot_password/` - Request password reset
- `POST /api/users/reset_password/` - Reset password with token
- `POST /api/users/create_api_key/` - Create API key

### Billing
- `GET /api/billing/plans/` - List subscription plans
- `GET /api/billing/subscriptions/current/` - Get current subscription
- `POST /api/billing/subscriptions/` - Create subscription
- `POST /api/billing/subscriptions/{id}/cancel/` - Cancel subscription
- `GET /api/billing/payments/` - List payments

### Tools
- `GET /api/tools/documents/` - List documents
- `POST /api/tools/documents/` - Upload document
- `GET /api/tools/digital-signatures/` - List digital signatures

## Environment Variables

Create a `.env` file with:
```
DJANGO_ENVIRONMENT=development
SECRET_KEY=your-secret-key
EMAIL_HOST_USER=your-email
EMAIL_HOST_PASSWORD=your-password
PAYSTACK_SECRET_KEY=your-paystack-key
PAYSTACK_PUBLIC_KEY=your-paystack-public-key
```

## Running the Application

```bash
# Development
python manage.py runserver

# With environment variable
DJANGO_ENVIRONMENT=development python manage.py runserver

# Production
DJANGO_ENVIRONMENT=production python manage.py runserver
```
