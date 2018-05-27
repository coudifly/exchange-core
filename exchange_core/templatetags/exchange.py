import json
import importlib

from django.template import Library
from django.conf import settings
from django.urls.resolvers import URLPattern

from exchange_core.utils import get_url_patterns


register = Library()

@register.filter(is_safe=True)
def serialize(data):
    return json.dumps(data)


# Armazena o nome das URLs para usar como referencia
pattern_names = get_url_patterns()
# Retorna um booleano identificando se a URL existe ou nao
@register.simple_tag
def ex_url_exists(pattern_name):
    if pattern_name in pattern_names:
        return True
    return False