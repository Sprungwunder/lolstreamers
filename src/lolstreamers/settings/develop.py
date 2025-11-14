
from .base import *

# In development, we use a fixed secret key
SECRET_KEY = 'django-insecure-9(d6((0u*o7b$xretw9k60w^x&l)rdg*9j$1s9ineiu#)x)yne'

# Debug should be True in development
DEBUG = True

# Allow all hosts in development
ALLOWED_HOSTS = []

# Use SQLite in development
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Development CORS settings - typically localhost
CORS_ALLOWED_ORIGINS = [
    "http://localhost:4200",  # Angular frontend
]

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:4200",  # Angular frontend
]

CORS_ALLOW_CREDENTIALS = True

# Development-specific JWT settings
SIMPLE_JWT.update({
    'AUTH_COOKIE_SECURE': False,  # Don't require HTTPS in development
})

# Development Elasticsearch settings
ELASTICSEARCH_DSL = {
    'default': {
        'hosts': [os.getenv("ELASTIC_HOST", 'http://localhost:9200')],
        'api_key': (
            os.getenv("ELASTIC_API_KEY_ID", 'default_key_id'),
            os.getenv("ELASTIC_API_KEY", 'default_key')
        ),
        'verify_certs': False,  # Don't verify SSL in development
        'ssl_show_warn': True
    },
}

# Email settings for development (if needed)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# No SSL redirect in development
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# Static files configuration
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'json': {
            '()': 'django_json_logging.formatters.JSONFormatter',
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'json',
        },
        'console_verbose': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'json',
        }
    },
    'loggers': {
        'google_api': {
            'handlers': ['console_verbose'],
            'level': 'DEBUG',
        },
        'lolstreamsearch.api': {
            'handlers': ['console_verbose'],
            'level': 'DEBUG',
        }
    }
}

RIOT_API_KEY = 'RGAPI-aec50855-7d77-42fa-bbf2-a741fd863174'
