from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django import forms
from django.core.files import File
from passwords.fields import PasswordField

import account.forms

from .models import Users, BankAccounts


class SignupForm(account.forms.SignupForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    password = PasswordField(label=_("Password"), strip=settings.ACCOUNT_PASSWORD_STRIP)
    
    field_order = ['first_name', 'last_name', 'username', 'email', 'password', 'password_confirm', 'code']


class ResetTokenForm(account.forms.PasswordResetTokenForm):
    password = PasswordField(label=_("Password"), strip=settings.ACCOUNT_PASSWORD_STRIP)


class AccountSettingsForm(account.forms.SettingsForm):
    form_name = forms.CharField(widget=forms.HiddenInput(), initial='settings')


class AvatarForm(forms.ModelForm):
    form_name = forms.CharField(widget=forms.HiddenInput(), initial='avatar')
    
    class Meta:
        model = Users
        fields = ('avatar',)


class BankAccountForm(forms.ModelForm):
    form_name = forms.CharField(widget=forms.HiddenInput(), initial='bank_account')

    class Meta:
        model = BankAccounts
        fields = ('bank', 'agency', 'account_type', 'account_number',)


class ChangePasswordForm(forms.Form):
    form_name = forms.CharField(widget=forms.HiddenInput(), initial='change_password')
    password = PasswordField(label=_("Password"), strip=settings.ACCOUNT_PASSWORD_STRIP)
    repeat_password = forms.CharField(widget=forms.PasswordInput())
    current_password = forms.CharField(widget=forms.PasswordInput())