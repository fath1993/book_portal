from book_portal.settings import *

SECRET_KEY = 'django-insecure-2=oal@8j309_e%6c@kn%c^jffbt4=k0hk9^&%6c!%&b$4x+h)y'

DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

STATIC_ROOT = BASE_DIR / 'static'
MEDIA_ROOT = BASE_DIR / 'media'

STATICFILES_DIRS = [
    BASE_DIR / "statics",
]