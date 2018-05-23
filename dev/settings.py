from dj_database_url import parse

from dev42.settings import *  # noqa
from dev42.settings import INSTALLED_APPS

SECRET_KEY = 'super secret shhhhh'
DEBUG = True

ALLOWED_HOSTS = ['web.dev42.vcap.me', '*', 'localhost']
INTERNAL_IPS = ['127.0.0.1', '172.19.0.1']

INSTALLED_APPS += [
    'wagtail.contrib.styleguide',
]

DATABASES = {
    'default': parse('postgres://postgres@database/postgres'),
}

DATA_ROOT = '/app/data/'
MEDIA_ROOT = DATA_ROOT + 'media/'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'mail'
EMAIL_PORT = 25
