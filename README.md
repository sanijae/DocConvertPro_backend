# DocConvertPro Backend API

A modern, modular Django REST Framework API for PDF conversion, document management, user authentication, and subscription billing.

## 🏗️ Architecture

The backend is structured into three main modular applications:

- **`apps/users`** - User authentication, registration, password management, API keys, and contact management
- **`apps/tools`** - PDF conversion tools, document processing, digital signatures, and OCR
- **`apps/billing`** - Subscription plans, user subscriptions, and payment processing

## ✨ Features

### User Management
- User registration and authentication
- Password reset functionality
- API key generation and management
- User profile management
- Contact form submissions

### PDF Conversion Tools
- **PDF to Other Formats**: Word, Excel, CSV, JPG, PNG, JPEG, BMP, PPT
- **Other Formats to PDF**: Word, Excel, CSV, Images, PPT
- **PDF Editing**: Extract pages, remove/add pages, repair, rotate, add watermarks
- **PDF Optimization**: Compress, merge, split PDFs
- **PDF Security**: Protect/unprotect PDFs, digital signatures
- **OCR**: Image OCR and identity document OCR

### Billing & Subscriptions
- Subscription plan management
- User subscription tracking
- Payment processing
- Conversion limit enforcement

## 🛠️ Tech Stack

- **Framework**: Django 4.2.13
- **API**: Django REST Framework 3.14.0
- **Database**: SQLite (development) / PostgreSQL (production)
- **Authentication**: Token-based authentication + API keys
- **PDF Processing**: PyPDF2, PyMuPDF, pdf2docx, reportlab
- **Image Processing**: Pillow, OpenCV, img2pdf
- **OCR**: pytesseract
- **Task Queue**: Celery (for background tasks)
- **CORS**: django-cors-headers

## 📋 Prerequisites

- Python 3.9+
- pip
- Virtual environment (recommended)
- Tesseract OCR (for OCR features)
  - **Windows**: Download from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)
  - **macOS**: `brew install tesseract`
  - **Linux**: `sudo apt-get install tesseract-ocr`

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd DocConvertPro_backend
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Variables

Create a `.env` file in the project root:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (for production, use PostgreSQL)
DATABASE_URL=sqlite:///db.sqlite3

# CORS Settings
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001

# Media & Static Files
MEDIA_ROOT=media
STATIC_ROOT=staticfiles

# Email Configuration (optional)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Celery (optional, for background tasks)
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

### 5. Database Setup

```bash
# Run migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser
```

### 6. Run Development Server

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/`

## 📚 API Endpoints

### Base URL
```
http://localhost:8000/api/
```

### API Root
```
GET /
```
Returns API information and available endpoints.

### Users API (`/api/users/`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/users/register/` | Register new user |
| POST | `/api/users/login/` | User login |
| POST | `/api/users/logout/` | User logout |
| POST | `/api/users/password-reset/` | Request password reset |
| POST | `/api/users/password-reset-confirm/` | Confirm password reset |
| GET | `/api/users/me/` | Get current user profile |
| PUT | `/api/users/me/` | Update user profile |
| POST | `/api/users/api-keys/` | Generate API key |
| GET | `/api/users/api-keys/` | List user API keys |
| DELETE | `/api/users/api-keys/{id}/` | Delete API key |
| POST | `/api/users/contacts/` | Submit contact form |

### Tools API (`/api/tools/`)

#### PDF to Other Formats
- `POST /api/tools/pdf-to-word/` - Convert PDF to Word
- `POST /api/tools/pdf-to-excel/` - Convert PDF to Excel
- `POST /api/tools/pdf-to-csv/` - Convert PDF to CSV
- `POST /api/tools/pdf-to-jpg/` - Convert PDF to JPG
- `POST /api/tools/pdf-to-png/` - Convert PDF to PNG
- `POST /api/tools/pdf-to-jpeg/` - Convert PDF to JPEG
- `POST /api/tools/pdf-to-bmp/` - Convert PDF to BMP
- `POST /api/tools/pdf-to-ppt/` - Convert PDF to PowerPoint

#### Other Formats to PDF
- `POST /api/tools/word-to-pdf/` - Convert Word to PDF
- `POST /api/tools/excel-to-pdf/` - Convert Excel to PDF
- `POST /api/tools/csv-to-pdf/` - Convert CSV to PDF
- `POST /api/tools/image-to-pdf/` - Convert Images to PDF
- `POST /api/tools/ppt-to-pdf/` - Convert PowerPoint to PDF

#### PDF Editing
- `POST /api/tools/extract-pdf/` - Extract pages from PDF
- `POST /api/tools/remove-pdf-page/` - Remove pages from PDF
- `POST /api/tools/add-pdf-page/` - Add pages to PDF
- `POST /api/tools/repair-pdf/` - Repair corrupted PDF
- `POST /api/tools/rotate-pdf/` - Rotate PDF pages
- `POST /api/tools/add-watermark/` - Add watermark to PDF

#### PDF Optimization
- `POST /api/tools/compress-pdf/` - Compress PDF file
- `POST /api/tools/merge-pdf/` - Merge multiple PDFs
- `POST /api/tools/split-pdf/` - Split PDF into multiple files

#### PDF Security
- `POST /api/tools/protect-pdf/` - Password protect PDF
- `POST /api/tools/unprotect-pdf/` - Remove PDF password
- `POST /api/tools/sign-pdf/` - Digitally sign PDF

#### OCR
- `POST /api/tools/ocr-image/` - OCR on images
- `POST /api/tools/ocr-identity/` - OCR on identity documents

#### Document Management
- `GET /api/tools/documents/` - List documents
- `POST /api/tools/documents/` - Upload document
- `GET /api/tools/documents/{id}/` - Get document details
- `DELETE /api/tools/documents/{id}/` - Delete document

#### Digital Signatures
- `GET /api/tools/digital-signatures/` - List signatures
- `POST /api/tools/digital-signatures/` - Create signature
- `GET /api/tools/digital-signatures/{id}/` - Get signature details
- `DELETE /api/tools/digital-signatures/{id}/` - Delete signature

### Billing API (`/api/billing/`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/billing/plans/` | List subscription plans |
| GET | `/api/billing/plans/{id}/` | Get plan details |
| GET | `/api/billing/subscriptions/` | List user subscriptions |
| POST | `/api/billing/subscriptions/` | Create subscription |
| GET | `/api/billing/subscriptions/{id}/` | Get subscription details |
| PUT | `/api/billing/subscriptions/{id}/` | Update subscription |
| GET | `/api/billing/payments/` | List payments |
| POST | `/api/billing/payments/` | Create payment record |
| GET | `/api/billing/payments/{id}/` | Get payment details |

## 🔐 Authentication

### Token Authentication

Include the token in the Authorization header:

```http
Authorization: Token <your-token-here>
```

### API Key Authentication

Include the API key in the X-API-KEY header:

```http
X-API-KEY: <your-api-key-here>
```

### Example Request

```bash
curl -X GET http://localhost:8000/api/users/me/ \
  -H "Authorization: Token <your-token>"
```

## 🗄️ Database

### Development (SQLite)
SQLite is used by default for development. No additional setup required.

### Production (PostgreSQL)

1. Install PostgreSQL
2. Create database:
```sql
CREATE DATABASE docconvertpro;
CREATE USER docconvertpro_user WITH PASSWORD 'your-password';
GRANT ALL PRIVILEGES ON DATABASE docconvertpro TO docconvertpro_user;
```

3. Update `.env`:
```env
DATABASE_URL=postgresql://docconvertpro_user:your-password@localhost:5432/docconvertpro
```

4. Run migrations:
```bash
python manage.py migrate
```

## 🧪 Testing

```bash
# Run all tests
python manage.py test

# Run tests for specific app
python manage.py test apps.users
python manage.py test apps.tools
python manage.py test apps.billing
```

## 📁 Project Structure

```
DocConvertPro_backend/
├── apps/
│   ├── users/          # User authentication & management
│   ├── tools/          # PDF conversion tools
│   └── billing/        # Subscription & billing
├── common/             # Shared utilities, exceptions, permissions
├── config/             # Django settings & configuration
│   └── settings/      # Environment-specific settings
├── media/             # Uploaded files
├── static/            # Static files
├── staticfiles/       # Collected static files
├── templates/         # HTML templates
├── scripts/           # Utility scripts
├── manage.py          # Django management script
└── requirements.txt   # Python dependencies
```

## 🔄 Background Tasks (Celery)

For background tasks like checking expired API keys and subscriptions:

1. Install Redis:
```bash
# macOS
brew install redis

# Linux
sudo apt-get install redis-server
```

2. Start Celery worker:
```bash
celery -A config worker -l info
```

3. Start Celery beat (for scheduled tasks):
```bash
celery -A config beat -l info
```

## 🚢 Deployment

### Production Settings

1. Set `DEBUG=False` in production settings
2. Update `ALLOWED_HOSTS` with your domain
3. Use PostgreSQL for production database
4. Configure proper CORS settings
5. Set up static file serving (e.g., WhiteNoise or CDN)
6. Use environment variables for sensitive data
7. Enable HTTPS
8. Set up proper logging

### Environment Variables for Production

```env
SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:password@host:5432/dbname
CORS_ALLOWED_ORIGINS=https://yourdomain.com
```

## 📝 API Documentation

Visit the API root endpoint for interactive documentation:
```
http://localhost:8000/
```

For detailed API documentation, use Django REST Framework's browsable API or integrate Swagger/OpenAPI.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is proprietary software. All rights reserved.

## 🆘 Support

For issues and questions:
- Open an issue on GitHub
- Contact: [your-email@example.com]

## 🔗 Related Documentation

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Migration Guide](./MIGRATION_GUIDE.md)
- [Endpoint Migration](./ENDPOINT_MIGRATION.md)

---

**Version**: 1.0.0  
**Last Updated**: 2024
