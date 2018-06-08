from django.utils.deprecation import MiddlewareMixin
from django.urls import reverse
from django.http import HttpResponsePermanentRedirect
from django.conf import settings

from session_security.middleware import SessionSecurityMiddleware

from exchange_core.models import Users


# Redirects the user if it yet not send the documents
class UserDocumentsMiddleware(MiddlewareMixin):
	ignore_paths = [
		'/' + settings.ADMIN_URL_PREFIX,
		reverse('set_language'),
		'/' + getattr(settings, 'SPONSORSHIP_URL_PREFIX', '0000000000'),
		reverse('core>logout'),
		reverse('core>documents'),
		reverse('core>settings'),
		reverse('core>get-regions'),
		reverse('core>get-cities'),
	]

	allowed_paths = []

	def must_ignore(self, request):
		if '.' in request.path:
			return True

		for path in (self.ignore_paths + settings.IGNORE_PATHS):
			if request.path.startswith(path) and path not in self.allowed_paths:
				return True
		return False

	def process_request(self, request):
		if not settings.REQUIRE_USER_DOCUMENTS:
			return
		if self.must_ignore(request):
			return
		if request.user.is_authenticated and (request.user.status == Users.STATUS.created or request.user.status == Users.STATUS.disapproved_documentation):
			return HttpResponsePermanentRedirect(reverse('core>documents'))


# Redirects the user if it yet not send the documents
class CheckUserLoggedInMiddleware(MiddlewareMixin):
	def process_request(self, request):
		if not request.path.startswith(reverse(settings.LOGIN_URL)):
			return
		if not request.user.is_authenticated:
			return
		return HttpResponsePermanentRedirect(settings.LOGIN_REDIRECT_URL)


class CoreSessionSecurityMiddleware(SessionSecurityMiddleware):
	def process_request(self, *args, **kwargs):
		super().process_request(*args, **kwargs)
