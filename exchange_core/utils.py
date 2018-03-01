import importlib

from django.conf import settings
from django.urls.resolvers import URLPattern


def get_url_patterns():
	pattern_names = []

	for app_name in settings.INSTALLED_APPS:
		if app_name.startswith('exchange_'):
			urls_module = importlib.import_module(app_name + '.urls')
			urlpatterns = getattr(urls_module, 'urlpatterns')
			
			for url in urlpatterns:
				if isinstance(url, URLPattern):
					pattern_names.append(url.pattern.name)

	return pattern_names