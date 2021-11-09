from .settings import *

DEBUG = False
TEMPLATES_DEBUG = False

ALLOWED_HOSTS = []


DATABASES['default'] = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'base14c',
            'USER': 'root',
            'PASSWORD': 'Password',
            'PORT': 3306,
            'HOST': '127.0.0.1'
    }
}

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')