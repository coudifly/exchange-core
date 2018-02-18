from django.template import Library
from django.conf import settings


register = Library()


@register.filter(is_safe=True)
def language_css_class(lang):
    if lang in settings.LANGUAGE_CSS_CLASSES:
    	return settings.LANGUAGE_CSS_CLASSES[lang]