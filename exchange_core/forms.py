from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django import forms
from django.core.files import File
from passwords.fields import PasswordField
from localflavor.br.forms import BRCPFField

import account.forms

from .models import Users, BankAccounts, Documents


class SignupForm(account.forms.SignupForm):
    first_name = forms.CharField(label=_("First name"))
    last_name = forms.CharField(label=_("Last name"))
    confirm_email = forms.EmailField(label=_("Confirm e-mail"))
    password = PasswordField(label=_("Password"), strip=settings.ACCOUNT_PASSWORD_STRIP)
    document_1 = BRCPFField(label=_("CPF"))
    document_2 = forms.CharField(label=_("RG"))
    
    field_order = ['first_name', 'last_name', 'username', 'email', 'confirm_email', 'password', 'password_confirm', 'code', 'document_1', 'document_2']

    # Valida o campo de confirmar e-mail
    def clean_confirm_email(self):
        email = self.cleaned_data.get('email')
        confirm_email = self.cleaned_data.get('confirm_email')

        if not email == confirm_email:
            raise forms.ValidationError(_("The e-mails aren't equal"))

        return confirm_email


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
    password = PasswordField(label=_("New Password"), strip=settings.ACCOUNT_PASSWORD_STRIP)
    repeat_password = forms.CharField(widget=forms.PasswordInput())
    current_password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def clean_repeat_password(self):
        password = self.cleaned_data['password']
        repeat_password = self.cleaned_data['repeat_password']

        if password != repeat_password:
            raise forms.ValidationError(_("The passwords aren't equals"))
        return repeat_password

    def clean_current_password(self):
        current_password = self.cleaned_data['current_password']

        if not self.user.check_password(current_password):
            raise forms.ValidationError(_("The passwords aren't equals"))
        return current_password


class DocumentForm(forms.ModelForm):
    form_name = forms.CharField(widget=forms.HiddenInput())
    
    class Meta:
        model = Documents
        fields = ('file',)