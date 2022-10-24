from book_portal.settings import *

with open('/etc/secret_key.txt') as f:
    SECRET_KEY = f.read().strip()

DEBUG = False

ALLOWED_HOSTS = ['localhost', 'domain.com', ]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {'charset': 'utf8mb4'},
        'NAME': 'sssmachi_db',
        'USER': 'sssmachi_db_user',
        'PASSWORD': 'hdf#1434GA283',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

STATIC_ROOT = 'path/to/directory/static'
MEDIA_ROOT = 'path/to/directory/media'

STATICFILES_DIRS = [
    BASE_DIR / "statics",
]
