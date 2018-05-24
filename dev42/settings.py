"""
Base Django settings for web.dev42.co.
"""
from pathlib import PurePosixPath

INSTALLED_APPS = [
    'dev42',
    'dev42.events',
    'dev42.frontend',
    'dev42.website',

    'wagtail.admin',
    'wagtail.core',
    'wagtail.documents',
    'wagtail.embeds',
    'wagtail.images',
    'wagtail.sites',
    'wagtail.snippets',
    'wagtail.users',
    'wagtail.contrib.settings',
    'wagtail.contrib.modeladmin',
    'modelcluster',
    'taggit',

    # Django apps
    'django.forms',
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'wagtail.core.middleware.SiteMiddleware',
]

ROOT_URLCONF = 'dev42.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'wagtail.contrib.settings.context_processors.settings',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
        },
    },
]
FORM_RENDERER = 'django.forms.renderers.TemplatesSetting'

WSGI_APPLICATION = 'dev42.wsgi.application'

# Trust nginx
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

LANGUAGE_CODE = 'en-au'
TIME_ZONE = 'Australia/Hobart'
USE_I18N = False
USE_L10N = False
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# Paths for the application
addslash = '{}/'.format
ROOT_URL = PurePosixPath('/')
ASSETS_URL = ROOT_URL / 'assets'
MEDIA_URL = addslash(ASSETS_URL / 'media')
STATIC_URL = addslash(ASSETS_URL / 'static')

EMAIL_SUBJECT_PREFIX = '[dev42] '


# Wagtail settings
WAGTAIL_SITE_NAME = 'dev42'
WAGTAIL_ENABLE_UPDATE_CHECK = False

WAGTAILADMIN_NOTIFICATION_USE_HTML = True
TAGGIT_CASE_INSENSITIVE = True


# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'mail_admins'],
            'propagate': True,
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}


# Google Maps API key
GOOGLE_MAPS_API_KEY =  "AIzaSyCz040KiMBXhkqsEb_UanP-yELmwqpwjHE"
