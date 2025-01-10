from pathlib import Path
from dotenv import load_dotenv
import os
import cloudinary
import cloudinary.uploader
import cloudinary.api

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY')


AUTH_USER_MODEL = 'userauth.CustomUser'

# Installed Apps
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'rest_framework',
    "display",
    "userauth",
    "EMAILapp",
    "SMSapp",
    "cart",
    'cloudinary',
    'cloudinary_storage',
    'chatbot',
    'corsheaders',
    'django_social_share',


]


# Middleware
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  
    'django.middleware.common.CommonMiddleware',
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

ROOT_URLCONF = "ECOM.urls"
WSGI_APPLICATION = "ECOM.wsgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                'display.context_processors.categories',

            ],
        },
    },
]


# Static & Media
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

SHARED_STORAGE = os.path.join(BASE_DIR, 'shared_storage')

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

# Twilio Configuration
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_VERIFY_SERVICE_SID = os.getenv('TWILIO_VERIFY_SERVICE_SID')
TWILIO_WHATSAPP_NUMBER = os.getenv('TWILIO_WHATSAPP_NUMBER')

# Stripe Configuration
STRIPE_PUBLIC_KEY = os.getenv('STRIPE_PUBLIC_KEY')
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')
STRIPE_WEBHOOK_SECRET = os.getenv('STRIPE_WEBHOOK_SECRET')

# API Keys
HUGGINGFACE_API_TOKEN = os.getenv('HUGGINGFACE_API_TOKEN')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"



cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)

##################   SECURITY SECITON   #################### 

# # For Security make false in production
DEBUG = True

# # Restrict Allowed Hosts
ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    '.ngrok-free.app',
    'f1a0-39-45-6-101.ngrok-free.app'

]
#will accept POST requests from this domains 
CSRF_TRUSTED_ORIGINS = [
    'https://f1a0-39-45-6-101.ngrok-free.app',
]


#CORS will not show error for these sites 
CORS_ALLOWED_ORIGINS = [
    'http://127.0.0.1:8000',
    'http://localhost:8000',
    'http://127.0.0.1:4040',
    'https://a9ad-39-45-6-101.ngrok-free.app',
]




#For Testing 
# # For Security make false in production
DEBUG = True
# Enforce HTTPS by redirecting HTTP to HTTPS
SECURE_SSL_REDIRECT = False
SECURE_HSTS_SECONDS = 0
# Use Secure Cookies but will not work if use cookies in authentication 
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
# Enable HSTS
SECURE_HSTS_SECONDS = 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False
# XSS Protection
SECURE_BROWSER_XSS_FILTER = True
# Clickjacking Protection
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = False
SESSION_COOKIE_SECURE = True      # Cookies sent over HTTPS only
SESSION_COOKIE_HTTPONLY = True    # Prevent JS access to cookies
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 1800         # 30 minutes
CSRF_COOKIE_SAMESITE = 'Lax'






# # For Production
# # For Security make false in production
# DEBUG = False
# Enforce HTTPS by redirecting HTTP to HTTPS
# SECURE_SSL_REDIRECT = True
# Use Secure Cookies but will not work if use cookies in authentication 
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# SECURE_HSTS_SECONDS = 31536000
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True
# XSS Protection
# SECURE_BROWSER_XSS_FILTER = True
# Clickjacking Protection
# X_FRAME_OPTIONS = 'DENY'
# SECURE_CONTENT_TYPE_NOSNIFF = True
# CSRF_COOKIE_SAMESITE = 'Lax'
