from .base import *


SESSION_ENGINE = 'redis_sessions.session'
# SESSION_REDIS_HOST = 'localhost'
# SESSION_REDIS_PORT = 6379

WS_PORT = 8888

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'chat',
        'USER': 'ubuntu',
        'PASSWORD': 'vagrant',
        'HOST': 'localhost',
        'PORT': '5432',
    },
}


STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
