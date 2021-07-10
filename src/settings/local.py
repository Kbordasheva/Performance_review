# flake8: noqa
from src.settings.base import *

INSTALLED_APPS.append('debug_toolbar')
MIDDLEWARE.insert(1, 'debug_toolbar.middleware.DebugToolbarMiddleware')
INTERNAL_IPS = [
    '127.0.0.1',
    '172.17.0.1'  # for Docker
]
