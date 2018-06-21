import json

from django.template import Library

from exchange_core.utils import get_url_patterns

register = Library()


@register.filter(is_safe=True)
def serialize(data):
    return json.dumps(data)


@register.filter(is_safe=True)
def decimal_slice(value, places=2):
    parts = '{:8f}'.format(value).split('.')
    return '{}.{}'.format(parts[0], parts[1][:places])


# Armazena o nome das URLs para usar como referencia
pattern_names = get_url_patterns()


# Retorna um booleano identificando se a URL existe ou nao
@register.simple_tag
def ex_url_exists(pattern_name):
    if pattern_name in pattern_names:
        return True
    return False
