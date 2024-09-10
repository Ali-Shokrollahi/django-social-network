from .base import *

ALLOWED_HOSTS = ['*']

DEVELOPMENT_APPS = [
    'debug_toolbar',
]

INTERNAL_IPS = [
    "127.0.0.1",
]

INSTALLED_APPS += DEVELOPMENT_APPS

MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')
