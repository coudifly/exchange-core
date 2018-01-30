from django.conf import settings


def exchange(request):
	return {
		'PROJECT_NAME': settings.PROJECT_NAME,
		'settings': settings
	}