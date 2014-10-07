# -*- coding: utf-8 -*-
"""
Django settings for d2f project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os, pwd
from os.path import join

# See: http://django-storages.readthedocs.org/en/latest/backends/amazon-S3.html#settings
try:
    from S3 import CallingFormat
    AWS_CALLING_FORMAT = CallingFormat.SUBDOMAIN
except ImportError:
    # TODO: Fix this where even if in Dev this class is called.
    pass

from configurations import Configuration, values

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
USER = pwd.getpwuid(os.getuid())[0]
PROJECT_NAME = os.environ.get('PROJECT_NAME', 'dtf')


class Common(Configuration):
    ########## APP CONFIGURATION
    DJANGO_APPS = (
        # Default Django apps:
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        'django.contrib.messages',
        'django.contrib.staticfiles',

        # Useful template tags:
        # 'django.contrib.humanize',

        # Admin
        'django.contrib.admin',
    )
    THIRD_PARTY_APPS = (
        'south',  # Database migration helpers:
        'crispy_forms',  # Form layouts
        'avatar',  # for user avatars
        'django_extensions',
        'tumblr_reader',
        'nufiles',
        'positions',
        'django_filters',
        'django_nose',
        'djnfusion',
        'django_comments',
        'sorl.thumbnail',
        'polymorphic',
        'djcelery',
        'localflavor',
        'django_hstore',
    )

    # Apps specific for this project go here.
    LOCAL_APPS = (
        'users',  # custom users app
        'pages',
        'blog',
        'facebook_groups',
        'app',
        'courses',
        'lessons',
        'tags',
        'resources',
        'profiles',
        'dtf_comments',
        'packages',
        'features',
        'journals',
        'affiliates',
        'etfars',
    )

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
    INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

    INSTALLED_APPS += (
        # Needs to come last for now because of a weird edge case between
        #   South and allauth
        'allauth',  # registration
        'allauth.account',  # registration
        'allauth.socialaccount',  # registration
        'allauth.socialaccount.providers.facebook',
    )
    INSTALLED_APPS += (
        'polymorphic',
        'django.contrib.contenttypes',
    )
    ########## END APP CONFIGURATION

    TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

    ########## MIDDLEWARE CONFIGURATION
    MIDDLEWARE_CLASSES = (
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    )
    ########## END MIDDLEWARE CONFIGURATION

    COMMENTS_APP = 'dtf_comments'

    ########## DEBUG
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
    DEBUG = values.BooleanValue(False)

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
    TEMPLATE_DEBUG = DEBUG
    ########## END DEBUG

    ########## SECRET CONFIGURATION
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
    # Note: This key only used for development and testing.
    #       In production, this is changed to a values.SecretValue() setting
    SECRET_KEY = "CHANGEME!!!"
    ########## END SECRET CONFIGURATION

    ########## FIXTURE CONFIGURATION
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-FIXTURE_DIRS
    FIXTURE_DIRS = (
        join(BASE_DIR, 'fixtures'),
    )
    ########## END FIXTURE CONFIGURATION

    ########## EMAIL CONFIGURATION
    EMAIL_BACKEND = values.Value('django.core.mail.backends.smtp.EmailBackend')
    ########## END EMAIL CONFIGURATION

    ########## MANAGER CONFIGURATION
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#admins
    ADMINS = (
        ('Will Farley', 'will@django.nu'),
    )

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#managers
    MANAGERS = ADMINS
    ########## END MANAGER CONFIGURATION

    ########## DATABASE CONFIGURATION
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
    DATABASES = values.DatabaseURLValue('postgres://localhost/trainings')
    ########## END DATABASE CONFIGURATION

    ########## CACHING
    # Do this here because thanks to django-pylibmc-sasl and pylibmc memcacheify is painful to install on windows.
    # memcacheify is what's used in Production
    CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': ''
        }
    }
    ########## END CACHING

    ########## GENERAL CONFIGURATION
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#time-zone
    TIME_ZONE = 'America/Phoenix'

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#language-code
    LANGUAGE_CODE = 'en-us'

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#site-id
    SITE_ID = 1

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
    USE_I18N = True

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
    USE_L10N = True

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
    USE_TZ = True
    ########## END GENERAL CONFIGURATION

    ########## TEMPLATE CONFIGURATION
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
    TEMPLATE_CONTEXT_PROCESSORS = (
        'django.contrib.auth.context_processors.auth',
        "allauth.account.context_processors.account",
        "allauth.socialaccount.context_processors.socialaccount",
        'django.core.context_processors.debug',
        'django.core.context_processors.i18n',
        'django.core.context_processors.media',
        'django.core.context_processors.static',
        'django.core.context_processors.tz',
        'django.contrib.messages.context_processors.messages',
        'django.core.context_processors.request',
        # Your stuff: custom template context processers go here
        'courses.context_processors.trainings_names',
    )

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
    TEMPLATE_DIRS = (
        join(BASE_DIR, 'templates'),
    )

    TEMPLATE_LOADERS = (
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        )

    # See: http://django-crispy-forms.readthedocs.org/en/latest/install.html#template-packs
    CRISPY_TEMPLATE_PACK = 'bootstrap3'
    ########## END TEMPLATE CONFIGURATION

    ########## STATIC FILE CONFIGURATION
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
    STATIC_ROOT = join(os.path.dirname(BASE_DIR), 'staticfiles')

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
    STATIC_URL = '/static/'

    # See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
    STATICFILES_DIRS = (
        join(BASE_DIR, 'static'),
    )

    # See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
    STATICFILES_FINDERS = (
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    )
    ########## END STATIC FILE CONFIGURATION

    ########## MEDIA CONFIGURATION
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
    MEDIA_ROOT = join(BASE_DIR, 'media')

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
    MEDIA_URL = '/media/'
    ########## END MEDIA CONFIGURATION

    ########## URL Configuration
    ROOT_URLCONF = 'config.urls'

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
    WSGI_APPLICATION = 'config.wsgi.application'
    ########## End URL Configuration

    ########## AUTHENTICATION CONFIGURATION
    AUTHENTICATION_BACKENDS = (
        "django.contrib.auth.backends.ModelBackend",
        "allauth.account.auth_backends.AuthenticationBackend",
    )

    # Some really nice defaults
    ACCOUNT_AUTHENTICATION_METHOD = "email"
    ACCOUNT_EMAIL_REQUIRED = True
    ACCOUNT_EMAIL_VERIFICATION = "mandatory"
    ACCOUNT_SIGNUP_FORM_CLASS = 'users.forms.UserSignupForm'
    SOCIALACCOUNT_AUTO_SIGNUP = False
    ########## END AUTHENTICATION CONFIGURATION

    ########## Custom user app defaults
    # Select the correct user model
    AUTH_USER_MODEL = "users.User"
    LOGIN_REDIRECT_URL = "users:redirect"
    ########## END Custom user app defaults

    ########## SLUGLIFIER
    AUTOSLUG_SLUGIFY_FUNCTION = "slugify.slugify"
    ########## END SLUGLIFIER

    ########## ELASTICSEARCH SETTINGS
    #BONSAI_URL = os.environ.get('BONSAI_URL', 'localhost')
    #ELASTICSEARCH_SETTINGS = [{'host': BONSAI_URL}]
    #ELASTICSEARCH_INDEX = os.environ.get('BONSAI_INDEX', 'dtf')

    ELASTICSEARCH_SETTINGS = [{'host': 'privet-1821403.us-east-1.bonsai.io',
                               'port': 443,
                               'use_ssl': True,
                               'username': 'ae3c3lfd',
                               'password': '61zwio5idcs8zyzi'
                               }]
    # Don't forget to create index in cluster.
    # Run: curl -XPUT 'url_to_elastic_search_cluster/index_name'
    ELASTICSEARCH_INDEX = 'dtf'
    
    ########## CELERY SETTINGS
    BROKER_URL = 'redis://localhost'
    CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'
    ########## END CELERY SETTINGS

    ########## LOGGING CONFIGURATION
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#logging
    # A sample logging configuration. The only tangible logging
    # performed by this configuration is to send an email to
    # the site admins on every HTTP 500 error when DEBUG=False.
    # See http://docs.djangoproject.com/en/dev/topics/logging for
    # more details on how to customize your logging configuration.
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'filters': {
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse'
            }
        },
        'handlers': {
            'mail_admins': {
                'level': 'ERROR',
                'filters': ['require_debug_false'],
                'class': 'django.utils.log.AdminEmailHandler'
            }
        },
        'loggers': {
            'django.request': {
                'handlers': ['mail_admins'],
                'level': 'ERROR',
                'propagate': True,
            },
        }
    }
    ########## END LOGGING CONFIGURATION


    ########## Your common stuff: Below this line define 3rd party libary settings
    INFUSIONSOFT_COMPANY = os.environ.get('INFUSIONSOFT_API_KEY', '')
    INFUSIONSOFT_API_KEY = os.environ.get('INFUSIONSOFT_API_KEY', '')
    ########## Djnfusion CONFIG

    DJNFUSION_COMPANY = os.environ.get('INFUSIONSOFT_COMPANY_ID', '')
    DJNFUSION_API_KEY = os.environ.get('INFUSIONSOFT_API_KEY', '')

    DJNFUSION_USERID_FIELD_NAME = 'infusionsoft_uid'
    # DJNFUSION_USER_ID_VALUE_PREPROCESSOR = lambda id: unicode(id)
    # DJNFUSION_ADDITIONAL_USER_FIELD_PROVIDER_CREATE = lambda u: dict()
    # DJNFUSION_ADDITIONAL_USER_FIELD_PROVIDER_UPDATE = lambda u: dict()
    # DJNFUSION_AUTO_OPTIN = False
    # DJNFUSION_OPTIN_ONLY_IF_ACTIVE = True
    # DJNFUSION_OPTIN_MESSAGE = 'Auto-optin through the Web application.'
    # DJNFUSION_DAILY_USER_STATISTICS = {}

    ########## SOCIAL CONFIG
    SOCIALACCOUNT_PROVIDERS = \
        { 'facebook':
              { 'SCOPE': ['email', 'public_profile', 'user_friends'],
                'AUTH_PARAMS': { 'auth_type': 'reauthenticate' },
                'METHOD': 'js_sdk',
                'VERIFIED_EMAIL': True
              }
        }
    ########## END SOCIAL CONFIG

    ########## SESSION CONFIG
    SESSION_COOKIE_AGE = 3600
    SESSION_SAVE_EVERY_REQUEST = True
    ########## SESSION CONFIG

    ########## AVATAR CONFIG
    AVATAR_MAX_AVATARS_PER_USER = 1
    AVATAR_AUTO_GENERATE_SIZES = (80, 300)
    AVATAR_HASH_USERDIRNAMES = True
    AVATAR_CLEANUP_DELETED = True
    AVATAR_HASH_FILENAMES = True
    AVATAR_MAX_SIZE = 1048576*2
    ########## END AVATAR CONFIG

    SOUTH_DATABASE_ADAPTERS = {'default': 'south.db.postgresql_psycopg2'}

    ########## START TRAININGS CONFIG
    COURSE_NAME = "Course"
    LESSON_NAME = "Lesson"
    RESOURCE_NAME = "Resource"
    HOMEWORK_NAME = "Homework"
    ########## END TRAININGS CONFIG

class Local(Common):

    ########## DEBUG
    DEBUG = values.BooleanValue(True)
    TEMPLATE_DEBUG = DEBUG
    ########## END DEBUG

    ########## INSTALLED_APPS
    INSTALLED_APPS = Common.INSTALLED_APPS
    ########## END INSTALLED_APPS

    ########## Mail settings
    EMAIL_HOST = "localhost"
    EMAIL_PORT = 1025
    EMAIL_BACKEND = values.Value('django.core.mail.backends.console.EmailBackend')
    ########## End mail settings

    ########## django-debug-toolbar
    MIDDLEWARE_CLASSES = Common.MIDDLEWARE_CLASSES + ('debug_toolbar.middleware.DebugToolbarMiddleware',)
    INSTALLED_APPS += ('debug_toolbar',)

    INTERNAL_IPS = ('127.0.0.1',)

    DEBUG_TOOLBAR_CONFIG = {
        'DISABLE_PANELS': [
            'debug_toolbar.panels.redirects.RedirectsPanel',
        ],
        'SHOW_TEMPLATE_CONTEXT': True,
    }
    ########## end django-debug-toolbar

    ########## Your local stuff: Below this line define 3rd party libary settings
    STATICFILES_DIRS = (
        join(BASE_DIR, 'static'),
        join(BASE_DIR, '..', 'bower_components'),
    )


class LocalAndrew(Local):
    # Andrews Local settings
    # $ export DJANGO_CONFIGURATION="LocalAndrew"
    DATABASES = values.DatabaseURLValue('postgres://postgres:postgres@localhost/dtf')

#     STATICFILES_STORAGE = DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

    # See: http://django-storages.readthedocs.org/en/latest/backends/amazon-S3.html#settings
    AWS_ACCESS_KEY_ID = 'AKIAICFP2ZVRVUMNSCLQ'
    AWS_SECRET_ACCESS_KEY = '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'
    AWS_STORAGE_BUCKET_NAME = 'dtf-heroku'



class Production(Common):

    ########## INSTALLED_APPS
    INSTALLED_APPS = Common.INSTALLED_APPS
    ########## END INSTALLED_APPS

    ########## SECRET KEY
    SECRET_KEY = values.SecretValue()
    ########## END SECRET KEY

    ########## django-secure
    INSTALLED_APPS += ("djangosecure",)

    # set this to 60 seconds and then to 518400 when you can prove it works
    MIDDLEWARE_CLASSES = Common.MIDDLEWARE_CLASSES + ('djangosecure.middleware.SecurityMiddleware',)
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_HSTS_SECONDS = 60
    SECURE_HSTS_INCLUDE_SUBDOMAINS = values.BooleanValue(True)
    SECURE_FRAME_DENY = values.BooleanValue(True)
    SECURE_CONTENT_TYPE_NOSNIFF = values.BooleanValue(True)
    SECURE_BROWSER_XSS_FILTER = values.BooleanValue(True)
    SESSION_COOKIE_SECURE = values.BooleanValue(True)
    SESSION_COOKIE_HTTPONLY = values.BooleanValue(True)
    SECURE_SSL_REDIRECT = values.BooleanValue(True)
    CSRF_COOKIE_SECURE = values.BooleanValue(True)

    ########## end django-secure

    ########## SITE CONFIGURATION
    # Hosts/domain names that are valid for this site
    # See https://docs.djangoproject.com/en/1.6/ref/settings/#allowed-hosts
    ALLOWED_HOSTS = ["*"]
    ########## END SITE CONFIGURATION

    INSTALLED_APPS += ("gunicorn",)

    ########## STORAGE CONFIGURATION
    # See: http://django-storages.readthedocs.org/en/latest/index.html
    INSTALLED_APPS += (
        'storages',
    )

    # See: http://django-storages.readthedocs.org/en/latest/backends/amazon-S3.html#settings
    STATICFILES_STORAGE = DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

    # See: http://django-storages.readthedocs.org/en/latest/backends/amazon-S3.html#settings
    AWS_ACCESS_KEY_ID = values.SecretValue()
    AWS_SECRET_ACCESS_KEY = values.SecretValue()
    AWS_STORAGE_BUCKET_NAME = values.SecretValue()
    AWS_AUTO_CREATE_BUCKET = True
    AWS_QUERYSTRING_AUTH = False

    # see: https://github.com/antonagestam/collectfast
    AWS_PRELOAD_METADATA = True
    INSTALLED_APPS += ("collectfast",)

    # AWS cache settings, don't change unless you know what you're doing:
    AWS_EXPIREY = 60 * 60 * 24 * 7
    AWS_HEADERS = {
        'Cache-Control': 'max-age=%d, s-maxage=%d, must-revalidate' % (AWS_EXPIREY,
            AWS_EXPIREY)
    }

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
    SSTATIC_URL = 'https://s3.amazonaws.com/%s/' % AWS_STORAGE_BUCKET_NAME
    MEDIA_URL = 'https://s3.amazonaws.com/%s/' % AWS_STORAGE_BUCKET_NAME
    ########## END STORAGE CONFIGURATION

    ########## EMAIL
    DEFAULT_FROM_EMAIL = values.Value(
            'd2f <noreply@localhost:8000>')
    EMAIL_HOST = values.Value('smtp.sendgrid.com')
    EMAIL_HOST_PASSWORD = values.SecretValue(environ_prefix="", environ_name="SENDGRID_PASSWORD")
    EMAIL_HOST_USER = values.SecretValue(environ_prefix="", environ_name="SENDGRID_USERNAME")
    EMAIL_PORT = values.IntegerValue(587, environ_prefix="", environ_name="EMAIL_PORT")
    EMAIL_SUBJECT_PREFIX = values.Value('[d2f] ', environ_name="EMAIL_SUBJECT_PREFIX")
    EMAIL_USE_TLS = True
    SERVER_EMAIL = EMAIL_HOST_USER
    ########## END EMAIL

    ########## TEMPLATE CONFIGURATION

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
    TEMPLATE_LOADERS = (
        ('django.template.loaders.cached.Loader', (
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        )),
    )
    ########## END TEMPLATE CONFIGURATION

    ########## CACHING
    # Only do this here because thanks to django-pylibmc-sasl and pylibmc memcacheify is painful to install on windows.
    try:
        # See: https://github.com/rdegges/django-heroku-memcacheify
        from memcacheify import memcacheify
        CACHES = memcacheify()
    except ImportError:
        CACHES = values.CacheURLValue(default="memcached://127.0.0.1:11211")
        os.environ['MEMCACHE_SERVERS'] = os.environ.get('MEMCACHIER_SERVERS', '').replace(',', ';')
#    os.environ['MEMCACHE_USERNAME'] = os.environ.get('MEMCACHIER_USERNAME', '')
#    os.environ['MEMCACHE_PASSWORD'] = os.environ.get('MEMCACHIER_PASSWORD', '')
#    CACHES = {
#      'default': {
#        'BACKEND': 'django_pylibmc.memcached.PyLibMCCache',
#        'TIMEOUT': 500,
#        'BINARY': True,
#        'OPTIONS': { 'tcp_nodelay': True }
#      }
#    }
    ########## END CACHING

    ########## Your production stuff: Below this line define 3rd party libary settings

    ########## Djnfusion CONFIG
    DJNFUSION_COMPANY = values.SecretValue(environ_prefix="", environ_name="INFUSIONSOFT_COMPANY_ID")
    DJNFUSION_API_KEY = values.SecretValue(environ_prefix="", environ_name="INFUSIONSOFT_API_KEY")
    ########## END Djnfusion CONFIG


    INFUSIONSOFT_COMPANY = values.SecretValue(environ_prefix="", environ_name="INFUSIONSOFT_COMPANY_ID")
    INFUSIONSOFT_API_KEY = values.SecretValue(environ_prefix="", environ_name="INFUSIONSOFT_COMPANY_ID")
    BROKER_URL = 'redis://redistogo:ae0406a227274aa7681acdf0fec01783@hoki.redistogo.com:11015/'
