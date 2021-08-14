# flake8: noqa
from src.settings.base import *

STATIC_URL = '/django_static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'django_static')

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
