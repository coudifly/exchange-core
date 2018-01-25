from decimal import Decimal
from json import JSONEncoder
from uuid import UUID

from django.conf import settings
from django.urls import reverse_lazy
from django.contrib import messages
from prettyconf.configuration import Configuration

# Diz ao pretty conf o path do .env caso não existam variáveis de ambiente para a respectiva config
config = Configuration(starting_path=settings.BASE_DIR)

# Reescreve o enconder Json padrão para suportar Decimal e UUID
JSONEncoder_default = JSONEncoder.default

def JSONEncoder_new(self, o):
    if isinstance(o, UUID): return str(o)
    if isinstance(o, Decimal): return round(float(o), 8)
    return JSONEncoder_olddefault(self, o)

JSONEncoder.default = JSONEncoder_new

# Define o nome do modulo
PACKAGE_NAME = 'exchange_core'

# Diz ao Django aonde está a configuração desse modulo
default_app_config = PACKAGE_NAME + '.apps.Config'

# Armazena o nome do projeto
settings.PROJECT_NAME = config('PROJECT_NAME')

# Dominio do site
settings.DOMAIN = config('DOMAIN', default='example.com')

# https://github.com/Bouke/django-two-factor-auth
# https://github.com/django-extensions/django-extensions
# https://github.com/jazzband/django-widget-tweaks
# https://github.com/pinax/django-user-accounts
# https://github.com/dstufft/django-passwords
# https://github.com/anymail/django-anymail
# https://github.com/yourlabs/django-session-security/
# django.contrib.sites é requerido pelo django-user-accounts
settings.INSTALLED_APPS += [
    'django.contrib.sites', 
	'django_otp',
    'django_otp.plugins.otp_static',
    'django_otp.plugins.otp_totp',
    'dj_pagination',
    'two_factor',
    'django_extensions',
    'widget_tweaks',
    'account',
    'anymail',
    'session_security',
    'easy_thumbnails',
]

# Adiciona os middlewares do Two Factor para habilitar a autenticação em dois passos
settings.MIDDLEWARE += [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_otp.middleware.OTPMiddleware',
    'account.middleware.LocaleMiddleware',
    'account.middleware.TimezoneMiddleware',
    'account.middleware.ExpiredPasswordMiddleware',
    'session_security.middleware.SessionSecurityMiddleware',
    'dj_pagination.middleware.PaginationMiddleware',
]

# Define a model do usuário como sendo a model Users desse modulo
settings.AUTH_USER_MODEL = PACKAGE_NAME + '.Users'

# Define o template do Two Factor para ser usado no login
settings.LOGIN_URL = 'two_factor:login'
settings.LOGIN_REDIRECT_URL = reverse_lazy('core>wallets')

# Adiciona o contexto do pacote django-user-accounts para os templates
# Adiciona o contexto do pacote django-session-security para os templates
# Adiciona o contexto para o nome do projeto
# Adiciona o contexto para as configuracoes do projeto
settings.TEMPLATES[0]['OPTIONS']['context_processors'] += [
    'account.context_processors.account',
    'exchange_core.context_processors.exchange',
]

# Define o ID do site
settings.SITE_ID = 1

# Django user accounts configurações
settings.ACCOUNT_LOGIN_URL = 'two_factor:login'
settings.ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = 'two_factor:login'
settings.ACCOUNT_PASSWORD_RESET_REDIRECT_URL = 'two_factor:login'
settings.ACCOUNT_SETTINGS_REDIRECT_URL = 'core>settings'
settings.ACCOUNT_EMAIL_UNIQUE = True
settings.ACCOUNT_EMAIL_CONFIRMATION_REQUIRED = True
settings.ACCOUNT_EMAIL_CONFIRMATION_URL = 'core>email-confirm'
settings.ACCOUNT_PASSWORD_EXPIRY = config('ACCOUNT_PASSWORD_EXPIRY', cast=int) # As senhas expiram em x dias e precisam ser trocas após esse tempo
settings.ACCOUNT_PASSWORD_USE_HISTORY = True

# Django Anymail configurações
settings.ANYMAIL = {
    'MAILGUN_API_KEY': config('MAILGUN_API_KEY'),
    'MAILGUN_SENDER_DOMAIN': config('MAILGUN_SENDER_DOMAIN'),
}

settings.DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')
settings.EMAIL_BACKEND = 'anymail.backends.mailgun.EmailBackend'

# Django session security configurações
settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = True
settings.SESSION_SECURITY_EXPIRE_AFTER = config('SESSION_SECURITY_EXPIRE_AFTER', cast=int) # Define o tempo de inatividade máximo do usuário, caso ele ultrapasse esse tempo, ele deverá fazer login novamente
settings.SESSION_SECURITY_WARN_AFTER = config('SESSION_SECURITY_WARN_AFTER', cast=int)

# Django passwords configurações
settings.PASSWORD_MIN_LENGTH = 8

# Django messages configurações / Alertas do bootstrap
settings.MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

# Configurações de armazenamento
settings.DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

settings.AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
settings.AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
settings.AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')

# Thumbnail configurações
settings.THUMBNAIL_DEFAULT_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
settings.THUMBNAIL_ALIASES = {
    '': {
        'avatar': {'size': (50, 50), 'crop': True},
    },
}

# Configurações do Real Brasileiro
settings.BRL_CURRENCY_SYMBOL = config('BRL_CURRENCY_SYMBOL', default='BRL')

# Static files configurações
settings.STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Opcoes de seguranca
settings.SECURE_HSTS_SECONDS = config('SECURE_HSTS_SECONDS', default=True, cast=config.boolean)
settings.SECURE_CONTENT_TYPE_NOSNIFF = config('SECURE_CONTENT_TYPE_NOSNIFF', default=True, cast=config.boolean)
settings.SECURE_BROWSER_XSS_FILTER = config('SECURE_BROWSER_XSS_FILTER', default=True, cast=config.boolean)
settings.SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=True, cast=config.boolean)
settings.SECURE_HSTS_PRELOAD = config('SESSION_COOKIE_SECURE', default=True, cast=config.boolean)
settings.SECURE_HSTS_INCLUDE_SUBDOMAINS = config('SESSION_COOKIE_SECURE', default=True, cast=config.boolean)
settings.SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default=True, cast=config.boolean)
settings.CSRF_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default=True, cast=config.boolean)
settings.X_FRAME_OPTIONS = config('X_FRAME_OPTIONS', default='DENY')

# Silencia os checks de seguranca do Django, caso configurado
settings.DISABLE_CHECKS = config('SESSION_COOKIE_SECURE', default=False, cast=config.boolean)

if settings.DISABLE_CHECKS:
    settings.SILENCED_SYSTEM_CHECKS = [
        'security.W001',
        'security.W002',
        'security.W003',
        'security.W004',
        'security.W005',
        'security.W006',
        'security.W007',
        'security.W008',
        'security.W009',
        'security.W010',
        'security.W011',
        'security.W012',
        'security.W013',
        'security.W014',
        'security.W015',
        'security.W016',
        'security.W017',
        'security.W018',
        'security.W019'
    ]