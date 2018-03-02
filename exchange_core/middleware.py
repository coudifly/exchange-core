from django.utils.deprecation import MiddlewareMixin
from django.urls import reverse
from django.http import HttpResponsePermanentRedirect
from django.conf import settings

from exchange_core.models import Users



# Redirects the user if it yet not send the documents 
class UserDocumentsMiddleware(MiddlewareMixin):
	ignore_paths = [
		'/admin',
		'/' + settings.SPONSORSHIP_URL_PREFIX,
		reverse('core>logout'),
		reverse('core>documents')
	]

	def process_request(self, request):
		print(request.path)
		if not settings.REQUIRE_USER_DOCUMENTS:
			return

		for path in self.ignore_paths:
			if request.path.startswith(path):
				return

		if request.user.is_authenticated and request.user.status == Users.STATUS.created:
			return HttpResponsePermanentRedirect(reverse('core>documents'))

