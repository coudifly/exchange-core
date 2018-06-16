import importlib

from django.conf import settings
from django.urls import include, path
from django.urls.resolvers import URLPattern
from django.db import connection
from functools import wraps


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


def close_db_connection(f):
    @wraps(f)
    def func_wrapper(*args, **kwargs):
        f_return = f(*args, **kwargs)
        connection.close()
        return f_return
    return func_wrapper


def generate_patterns(urlpatterns):
    for app_name in settings.INSTALLED_APPS:
        if app_name.startswith('exchange_'):
            urls_path = app_name + '.urls'
            urlpatterns.append(path('', include(urls_path)))
    return urlpatterns