from django.conf import settings
from django_otp import user_has_device


def exchange(request):
	return {
		'PROJECT_NAME': settings.PROJECT_NAME,
		'USER_HAS_DEVICE': lambda: user_has_device(request.user),
		'BRL_CURRENCY_SYMBOL': settings.BRL_CURRENCY_SYMBOL,
		'DOMAIN': settings.DOMAIN,
		'SPONSORSHIP_URL_PREFIX': settings.SPONSORSHIP_URL_PREFIX,
		'BR_DEPOSIT_MIN': settings.BR_DEPOSIT_MIN,
		'BR_DEPOSIT_MAX': settings.BR_DEPOSIT_MAX,
		'BR_DEPOSIT_DAILY_LIMIT': settings.BR_DEPOSIT_DAILY_LIMIT
	}