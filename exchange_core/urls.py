from django.urls import re_path, path, include
from django.conf import settings
from django.contrib import admin
from two_factor.urls import urlpatterns as tf_urls
from account.views import ConfirmEmailView, PasswordResetView, LogoutView, SettingsView

from . import views


urlpatterns = [
	# URLs do admin
	path(settings.ADMIN_URL_PREFIX, admin.site.urls),

	# i18n
	path('i18n/', include('django.conf.urls.i18n')),

	# URLs de terceiros
	re_path(r'', include(tf_urls)),
	re_path(r'session_security/', include('session_security.urls')),

	# URLs do pacote
	path('', views.HomeView.as_view(), name='core>home'),
	path('account/reset-password/', views.ResetPasswordView.as_view(), name='core>reset-password'),
	path('account/resend-confirmation-email/', views.ResendConfirmationEmailView.as_view(), name='core>resend-confirmation-email'),
	path('account/reset-token/<uidb36>/<token>/', views.ResetTokenView.as_view(), name='core>reset-token'),
	path('account/wallets/', views.WalletsView.as_view(), name='core>wallets'),
	path('account/email-confirm/<key>/', ConfirmEmailView.as_view(), name='core>email-confirm'),
	path('account/documents/', views.DocumentsView.as_view(), name='core>documents'),
	path('account/settings/', views.AccountSettingsView.as_view(), name='core>settings'),
	path('account/statement/', views.StatementView.as_view(), name='core>statement'),
	path('account/logout/', LogoutView.as_view(), name='core>logout'),

	# URLs de endereco
	path('address/get-regions/', views.GetRegionsView.as_view(), name='core>get-regions'),	
	path('address/get-cities/', views.GetCitiesView.as_view(), name='core>get-cities'),	
]

if settings.ENABLE_SIGNUP:
	urlpatterns.append(path('account/signup/', views.SignupView.as_view(), name='core>signup'))