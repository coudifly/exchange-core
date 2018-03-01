from django.utils.deprecation import MiddlewareMixin
from django.urls import reverse
from django.http import HttpResponsePermanentRedirect

from exchange_core.models import Users


# Redirects the user if it yet not send the documents 
class UserDocumentsMiddleware(MiddlewareMixin):
	def process_request(self, request):
		documents_path = reverse('core>documents')

		user_is_authenticated = request.user.is_authenticated
		user_has_created_status = user_is_authenticated and request.user.status == Users.STATUS.created
		documents_page = documents_path in request.path
		is_admin = request.path.startswith('/admin')
		is_logout = request.path.startswith(reverse('core>logout'))

		if user_is_authenticated and user_has_created_status and not documents_page \
			and not is_admin and not is_logout:
			return HttpResponsePermanentRedirect(documents_path)

