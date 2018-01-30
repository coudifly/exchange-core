from django.conf import settings
from django_otp import user_has_device


def exchange(request):
	return {
		'PROJECT_NAME': settings.PROJECT_NAME,
		'USER_HAS_DEVICE': lambda: user_has_device(request.user),
		'settings': settings
	}