from django.utils.deprecation import MiddlewareMixin
from django.urls import reverse
from django.http import HttpResponsePermanentRedirect

from exchange_core.models import Users


class UserDocumentsMiddleware(MiddlewareMixin):
	def process_request(self, request):
		documents_path = reverse('core>documents')
		
		user_is_authenticated = request.user.is_authenticated
		user_has_created_status = request.user.status == Users.STATUS.created
		documents_page = documents_path in request.path

		if user_is_authenticated and user_has_created_status and not documents_page:
			return HttpResponsePermanentRedirect(documents_path)

