from django.conf import settings
from django_otp import user_has_device


def exchange(request):
    return {
        'PROJECT_NAME': settings.PROJECT_NAME,
        'USER_HAS_DEVICE': lambda: user_has_device(request.user),
        'BRL_CURRENCY_CODE': settings.BRL_CURRENCY_CODE,
        'GOOGLE_ANALYTICS_TRACK_ID': settings.GOOGLE_ANALYTICS_TRACK_ID,
        'DOMAIN': settings.DOMAIN,
        'BR_DEPOSIT_MIN': settings.BR_DEPOSIT_MIN,
        'BR_DEPOSIT_MAX': settings.BR_DEPOSIT_MAX,
        'BR_DEPOSIT_DAILY_LIMIT': settings.BR_DEPOSIT_DAILY_LIMIT,
        'DEFAULT_ADDRESS_COUNTRY': settings.DEFAULT_ADDRESS_COUNTRY,
    }
