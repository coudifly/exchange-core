import os
import dj_database_url
import django_otp.plugins.otp_totp

from decimal import Decimal
from json import JSONEncoder
from uuid import UUID

from django.conf import settings
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import redirect
from django.urls import reverse
from prettyconf.configuration import Configuration

from exchange_core.casts import pairs, redis_url

# Tells to prettyconf  the path of .env in case of env vars not exists for given configuration
config = Configuration(starting_path=settings.BASE_DIR)

# Overwrite default Json encoder for Decimal and UUID support
JSONEncoder_default = JSONEncoder.default


def JSONEncoder_new(self, o):
    if isinstance(o, UUID):
        return str(o)
    if isinstance(o, Decimal):
        return format(o, '.8f')
    return JSONEncoder_default(self, o)


JSONEncoder.default = JSONEncoder_new

# Define the module name
PACKAGE_NAME = 'exchange_core'

# Monkey patch default_app_config django_otp
django_otp.plugins.otp_totp.default_app_config = PACKAGE_NAME + '.apps.OTPConfig'

# Tells to django where is the module config class
default_app_config = PACKAGE_NAME + '.apps.Config'

# Stores the project name
settings.PROJECT_NAME = config('PROJECT_NAME')

# System admins receive the email errors
settings.ADMINS = [(v, v)
                   for v in config('ADMINS', default=[], cast=config.list)]

# Configure the default home view for be visualized by the users
settings.HOME_VIEW = config('HOME_VIEW', default='core>wallets')

# Configure the Google Analytics tracking id
settings.GOOGLE_ANALYTICS_TRACK_ID = config(
    'GOOGLE_ANALYTICS_TRACK_ID', default=None)

# Configure the obligation for require the user documents from users new account
settings.REQUIRE_USER_DOCUMENTS = config(
    'REQUIRE_USER_DOCUMENTS', default=True, cast=config.boolean)

# URLs who should be ignored by the exchange middlewares
settings.IGNORE_PATHS = config('IGNORE_PATHS', default=[], cast=config.list)

# Site domain
settings.DOMAIN = config('DOMAIN', default='example.com')

# Enable/disable signup
settings.ENABLE_SIGNUP = config(
    'ENABLE_SIGNUP', default=True, cast=config.boolean)

# https://github.com/Bouke/django-two-factor-auth
# https://github.com/django-extensions/django-extensions
# https://github.com/jazzband/django-widget-tweaks
# https://github.com/pinax/django-user-accounts
# https://github.com/dstufft/django-passwords
# https://github.com/anymail/django-anymail
# https://github.com/yourlabs/django-session-security/
# django.contrib.sites is required by django-user-accounts
settings.INSTALLED_APPS += [
    'django.contrib.humanize',
    'django.contrib.sites',
    'django_otp',
    'django_otp.plugins.otp_static',
    'django_otp.plugins.otp_totp',
    'dj_pagination',
    'simple_history',
    'two_factor',
    'django_extensions',
    'widget_tweaks',
    'account',
    'anymail',
    'session_security',
    'easy_thumbnails',
    'cities',
    'mathfilters',
]

# Add the Two Factor middlewares for enable two steps authentication
settings.MIDDLEWARE += [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_otp.middleware.OTPMiddleware',
    'account.middleware.ExpiredPasswordMiddleware',
    'exchange_core.middleware.CoreSessionSecurityMiddleware',
    'exchange_core.middleware.UserDocumentsMiddleware',
    'exchange_core.middleware.CheckUserLoggedInMiddleware',
    'dj_pagination.middleware.PaginationMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
]

# Defines the user default Model
settings.AUTH_USER_MODEL = PACKAGE_NAME + '.Users'

# Defines the two factor template to be used for login
settings.LOGIN_URL = 'two_factor:login'
settings.LOGIN_REDIRECT_URL = reverse_lazy(
    config('LOGIN_REDIRECT_URL', default='core>wallets'))

# Database config
settings.DATABASES['default'] = dj_database_url.parse(config('DATABASE_URL'))
settings.DATABASES['default']['ENGINE'] = 'django.contrib.gis.db.backends.postgis'

# Redis session config
settings.SESSION_REDIS = config('REDIS_URL', default=None, cast=redis_url)

if settings.SESSION_REDIS:
    settings.SESSION_ENGINE = 'redis_sessions.session'

# Adds django-user-accounts to the templates context
# Adds django-session-security to the templates context
# Adds the context for project configurations
settings.TEMPLATES[0]['OPTIONS']['context_processors'] += [
    'account.context_processors.account',
    'exchange_core.context_processors.exchange',
]

settings.TEMPLATES[0]['DIRS'] = [
    os.path.join(settings.BASE_DIR, 'templates'),
    os.path.join(os.path.dirname(__file__), 'templates'),
]

# Defines default site id
settings.SITE_ID = 1

# Django-user-accounts config
settings.ACCOUNT_LOGIN_URL = 'two_factor:login'
settings.ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = 'two_factor:login'
settings.ACCOUNT_PASSWORD_RESET_REDIRECT_URL = 'two_factor:login'
settings.ACCOUNT_SETTINGS_REDIRECT_URL = 'core>settings'
settings.ACCOUNT_EMAIL_UNIQUE = True
settings.ACCOUNT_EMAIL_CONFIRMATION_REQUIRED = True
settings.ACCOUNT_EMAIL_CONFIRMATION_URL = 'core>email-confirm'
settings.ACCOUNT_PASSWORD_EXPIRY = config('ACCOUNT_PASSWORD_EXPIRY',
                                          cast=int)  # As senhas expiram em x dias e precisam ser trocas após esse tempo
settings.ACCOUNT_PASSWORD_USE_HISTORY = False

# Django Anymail config
settings.ANYMAIL = {
    'MAILGUN_API_KEY': config('MAILGUN_API_KEY'),
    'MAILGUN_SENDER_DOMAIN': config('MAILGUN_SENDER_DOMAIN'),
}

settings.SERVER_EMAIL = config('SERVER_EMAIL', default='server@example.com')

settings.DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')
settings.EMAIL_BACKEND = 'anymail.backends.mailgun.EmailBackend'

# Django session security config
settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = True
settings.SESSION_SECURITY_EXPIRE_AFTER = config('SESSION_SECURITY_EXPIRE_AFTER',
                                                cast=int)  # Define o tempo de inatividade máximo do usuário, caso ele ultrapasse esse tempo, ele deverá fazer login novamente
settings.SESSION_SECURITY_WARN_AFTER = config(
    'SESSION_SECURITY_WARN_AFTER', cast=int)

# Django passwords config
settings.PASSWORD_MIN_LENGTH = 8

# Django messages config/ bootstrap alerts
settings.MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

# Storage config
settings.DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

settings.AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
settings.AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
settings.AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')

# Thumbnail config
settings.THUMBNAIL_DEFAULT_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
settings.THUMBNAIL_ALIASES = {
    '': {
        'avatar': {'size': (50, 50), 'crop': True},
    },
}

# Static files config
settings.STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Security options
settings.SECURE_HSTS_SECONDS = config(
    'SECURE_HSTS_SECONDS', default=True, cast=config.boolean)
settings.SECURE_CONTENT_TYPE_NOSNIFF = config(
    'SECURE_CONTENT_TYPE_NOSNIFF', default=True, cast=config.boolean)
settings.SECURE_BROWSER_XSS_FILTER = config(
    'SECURE_BROWSER_XSS_FILTER', default=True, cast=config.boolean)
settings.SECURE_SSL_REDIRECT = config(
    'SECURE_SSL_REDIRECT', default=True, cast=config.boolean)
settings.SECURE_HSTS_PRELOAD = config(
    'SECURE_HSTS_PRELOAD', default=True, cast=config.boolean)
settings.SECURE_HSTS_INCLUDE_SUBDOMAINS = config(
    'SECURE_HSTS_INCLUDE_SUBDOMAINS', default=True, cast=config.boolean)
settings.SESSION_COOKIE_SECURE = config(
    'SESSION_COOKIE_SECURE', default=True, cast=config.boolean)
settings.SESSION_COOKIE_HTTPONLY = config(
    'SESSION_COOKIE_HTTPONLY', default=True, cast=config.boolean)
settings.CSRF_COOKIE_SECURE = config(
    'CSRF_COOKIE_SECURE', default=True, cast=config.boolean)
settings.CSRF_COOKIE_HTTPONLY = config(
    'CSRF_COOKIE_HTTPONLY', default=True, cast=config.boolean)
settings.X_FRAME_OPTIONS = config('X_FRAME_OPTIONS', default='DENY')

# Configure the URL prefix for exchange admin
settings.ADMIN_URL_PREFIX = config('ADMIN_URL_PREFIX', default='admin/')

# I18N config
settings.LANGUAGE_CSS_CLASSES = config(
    'LANGUAGE_CSS_CLASSES', default='', cast=pairs)
settings.LOCALE_PATHS = (os.path.join(settings.BASE_DIR, 'locale'),)
settings.LANGUAGE_CODE = 'en'
settings.LANGUAGES = [
    ('en', _('English')),
    ('pt-br', _('Portuguese')),
    ('es', _('Spanish')),
]

# L10N config
settings.USE_L10N = True
settings.USE_THOUSAND_SEPARATOR = True

# GDAL library config
settings.GDAL_LIBRARY_PATH = config('GDAL_LIBRARY_PATH', default=None)
settings.GEOS_LIBRARY_PATH = config('GEOS_LIBRARY_PATH', default=None)

# Django cities config
# https://github.com/coderholic/django-cities
settings.CITIES_LOCALES = ['LANGUAGES']
settings.CITIES_POSTAL_CODES = []
settings.CITIES_SKIP_CITIES_WITH_EMPTY_REGIONS = True
settings.DEFAULT_ADDRESS_COUNTRY = config(
    'DEFAULT_ADDRESS_COUNTRY', default=3469034)

# https://docs.djangoproject.com/en/2.0/ref/settings/#csrf-failure-view
settings.CSRF_FAILURE_VIEW = lambda *args, **kwargs: redirect(
    reverse(settings.LOGIN_REDIRECT_URL))
