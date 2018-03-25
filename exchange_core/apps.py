from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class Config(AppConfig):
	name = 'exchange_core'
	verbose_name = _('Exchange')

	def ready(self):
		import exchange_core.signals
		import exchange_core.unregister


class OTPConfig(AppConfig):
	name = 'django_otp.plugins.otp_totp'
	verbose_name = _("Two Factor Authentication")