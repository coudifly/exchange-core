from uuid import UUID
from decimal import Decimal

from django.http import JsonResponse as DjangoJsonResponse
from django.core.serializers.json import DjangoJSONEncoder


class CustomJSONEncoder(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o, UUID): return str(o)
        if isinstance(o, Decimal): return format(o, '.8f')
        return super().default(o)


class JsonResponse(DjangoJsonResponse):
    def __init__(self, *args, **kwargs):
        kwargs['encoder'] = CustomJSONEncoder
        return super().__init__(*args, **kwargs)
