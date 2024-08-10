from .base import *

ALLOWED_HOSTS = ['*']

DEVELOPMENT_APPS = [
    'debug_toolbar',
]

INTERNAL_IPS = [
    "127.0.0.1",
]

SITE_URL = 'http://localhost:8000'

INSTALLED_APPS += DEVELOPMENT_APPS

MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')

# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = False
FROM_EMAIL = 'ali.shokrollahi.me@gmail.com'
