"""
Django settings for pdf_office project.

Generated by 'django-admin startproject' using Django 5.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os
import certifi
from corsheaders.defaults import default_headers

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = os.path.join(BASE_DIR,"templates")

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    # os.path.join(BASE_DIR, "static"),
    BASE_DIR / "static"
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# MEDIA_DIR = os.path.join(BASE_DIR,'media')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-)3w56-%0obnb3$k&9n(#=r!9!fnd-&^=89altjt@%22qw!n!9+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

BASE_HOST_URL = 'http://localhost:3000/'
ALLOWED_HOSTS = ['127.0.0.1','http://localhost:3000/']

os.environ['SSL_CERT_FILE'] = certifi.where()
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'pdf_app'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES':[
        'rest_framework.permissions.AllowAny',
        # 'rest_framework.permissions.IsAuthenticated',
    ],

    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    }

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]

CORS_ALLOW_HEADERS = list(default_headers) + [
    'Api-Key',
]

# Additional settings as needed
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

ROOT_URLCONF = 'pdf_office.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'pdf_office.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

INTERNAL_IPS = ['127.0.0.1', '::1']


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_FILE_PATH = BASE_DIR / "sent_emails"
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True 
DEFAULT_FROM_EMAIL = 'DocConvertPro'
EMAIL_HOST_USER = 'datawareanalytics@gmail.com'  
EMAIL_HOST_PASSWORD =  'ztecrywnnphtzgoq' 


# PASSWORD_HASHERS = (
#     'pdf_app.hashers.MyPBKDF2PasswordHasher',
#     'django.contrib.auth.hashers.PBKDF2PasswordHasher',
#     'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
#     'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
#     'django.contrib.auth.hashers.BCryptPasswordHasher',
#     'django.contrib.auth.hashers.SHA1PasswordHasher',
#     'django.contrib.auth.hashers.MD5PasswordHasher',
#     'django.contrib.auth.hashers.CryptPasswordHasher',
# )
# AUTH_USER_MODEL = 'pdf_app.UsersModel'

## Payment setting ##

# Paystack
PAYSTACK_SECRET_KEY = 'sk_test_fa23fe07f8dc3ca7e4528f0e3a05fdb06075acb2'
PAYSTACK_PUBLIC_KEY = 'pk_test_60cab5dcb337717cb0d38c5991080ae13c9d6cea'
PAYSTACK_URL = "https://api.paystack.co/transaction/initialize"

# PayPal
PAYPAL_CLIENT_ID = 'AQ1ru6PBGsRLsywbjjeiJapWHzPIl9x8tu_mqQj64DKsrp_tYL0Fy7k0D6uEd_Fh4KLPAuf2lHZKqOUg'
PAYPAL_SECRET_KEY = 'EKXOLZ9N7xTCqZb4lDlDwHfY-46spmF3fO26sV-_KHkZUYBglRbX7i38IZnsyHM4HA8zTm5hlkOL1MKX'
PAYPAL_BASE_URL='https://api.sandbox.paypal.com'

# API_KEY_CUSTOM_HEADER = "HTTP_X_API_KEY"

