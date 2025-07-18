
from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

# Disable debug mode
DEBUG = False

# Define allowed hosts
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')

# Disable Swagger UI in production
SWAGGER_SETTINGS = {
    'ENABLED': False,
}

REST_FRAMEWORK = {
    **REST_FRAMEWORK,  # Keep existing REST_FRAMEWORK settings
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ]
}


# Use SQLite for testing
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
# Production database settings (PostgreSQL recommended)
#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.postgresql',
#        'NAME': os.getenv('DB_NAME'),
#        'USER': os.getenv('DB_USER'),
#        'PASSWORD': os.getenv('DB_PASSWORD'),
#        'HOST': os.getenv('DB_HOST'),
#        'PORT': os.getenv('DB_PORT', '5432'),
#        'CONN_MAX_AGE': 600,  # Connection persistence
#    }
#}

# Production CORS settings
CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS', '').split(',')
CSRF_TRUSTED_ORIGINS = os.getenv('CSRF_TRUSTED_ORIGINS', '').split(',')
CORS_ALLOW_CREDENTIALS = True

# Security settings
SECURE_SSL_REDIRECT = False
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# JWT settings for production
SIMPLE_JWT.update({
    'AUTH_COOKIE_SECURE': True,
    'AUTH_COOKIE_SAMESITE': 'Strict',
    'AUTH_COOKIE_DOMAIN': os.getenv('JWT_COOKIE_DOMAIN'),
})

# Elasticsearch production settings
ELASTICSEARCH_DSL = {
    'default': {
        'hosts': [os.getenv('ELASTIC_HOST')],
        'api_key': (
            os.getenv('ELASTIC_API_KEY_ID'),
            os.getenv('ELASTIC_API_KEY')
        ),
        'verify_certs': True,
        'ca_certs': '/app/certs/http_ca.crt',
        'ssl_show_warn': False,
        'timeout': 30,
        'retry_on_timeout': True,
        'max_retries': 3,
    }
}

# Static files configuration
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = os.getenv('STATIC_URL', '/static/')

# Media files configuration
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = os.getenv('MEDIA_URL', '/media/')

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'django.log'),
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

# Required environment variables check
REQUIRED_ENV_VARS = [
    'DJANGO_SECRET_KEY',
    'ELASTIC_HOST',
    'ELASTIC_API_KEY_ID',
    'ELASTIC_API_KEY',
    'ALLOWED_HOSTS',
    'CORS_ALLOWED_ORIGINS',
    'CSRF_TRUSTED_ORIGINS'
]

for var in REQUIRED_ENV_VARS:
    if not os.getenv(var):
        raise Exception(f'Required environment variable "{var}" is not set')
