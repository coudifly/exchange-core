from django.utils.deprecation import MiddlewareMixin
from django.urls import reverse
from django.http import HttpResponsePermanentRedirect
from django.conf import settings

from session_security.middleware import SessionSecurityMiddleware

from exchange_core.models import Users



# Redirects the user if it yet not send the documents
class UserDocumentsMiddleware(MiddlewareMixin):
	ignore_paths = [
		'/admin',
		reverse('set_language'),
		'/' + getattr(settings, 'SPONSORSHIP_URL_PREFIX', '0000000000'),
		reverse('core>logout'),
		reverse('core>documents'),

	]

	def process_request(self, request):
		if not settings.REQUIRE_USER_DOCUMENTS:
			return

		for path in self.ignore_paths:
			if request.path.startswith(path):
				return
		if (request.user.is_authenticated and request.user.status == Users.STATUS.created) or (request.user.is_authenticated and request.user.status == Users.STATUS.disapproved_documentation):
			return HttpResponsePermanentRedirect(reverse('core>documents'))


# Redirects the user if it yet not send the documents
class CheckUserLoggedInMiddleware(MiddlewareMixin):
	def process_request(self, request):
		if not request.path.startswith(reverse(settings.LOGIN_URL)):
			return
		if not request.user.is_authenticated:
			return
		return HttpResponsePermanentRedirect(reverse('core>wallets'))


class CoreSessionSecurityMiddleware(SessionSecurityMiddleware):
	def process_request(self, *args, **kwargs):
		super().process_request(*args, **kwargs)
