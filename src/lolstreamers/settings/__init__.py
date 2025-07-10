import os

# Default to development settings
environment = os.getenv('DJANGO_ENV', 'develop')

if environment == 'production':
    from .production import *
else:
    from .develop import *
