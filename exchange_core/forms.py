from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django import forms
from django.core.files import File
from passwords.fields import PasswordField
from localflavor.br.forms import BRCPFField

import account.forms

from exchange_core.mixins import RequiredFieldsMixin
from exchange_core.models import Users, BankAccounts, Documents, Addresses
from cities.models import Country, Region, City


class SignupForm(account.forms.SignupForm):
    first_name = forms.CharField(label=_("First name"))
    last_name = forms.CharField(label=_("Last name"))
    confirm_email = forms.EmailField(label=_("Confirm e-mail"))
    password = PasswordField(label=_("Password"), strip=settings.ACCOUNT_PASSWORD_STRIP)
    document_1 = BRCPFField(label=_("CPF"))
    document_2 = forms.CharField(label=_("RG"))
    mobile_phone = forms.CharField(label=_("Mobile phone"))
    
    field_order = ['first_name', 'last_name', 'username', 'mobile_phone',  'email', 'confirm_email', 'password', 'password_confirm', 'code', 'document_1', 'document_2']

    # Valida o campo de confirmar e-mail
    def clean_confirm_email(self):
        email = self.cleaned_data.get('email')
        confirm_email = self.cleaned_data.get('confirm_email')

        if not email == confirm_email:
            raise forms.ValidationError(_("The e-mails aren't equal"))

        return confirm_email


class AddressForm(forms.ModelForm):
    country = forms.ModelChoiceField(label=_("Country"), queryset=Country.objects.all(), empty_label=_("-- Select your country --"), initial=3469034, required=True)
    region = forms.ModelChoiceField(label=_("State"), queryset=Region.objects.none(), required=True)
    city = forms.ModelChoiceField(label=_("City"), queryset=Region.objects.none(), required=True)

    def __init__(self, *args, **kwargs):
        country = kwargs.pop('country')
        region = kwargs.pop('region')

        super().__init__(*args, **kwargs)
        
        if country and region:
            self.fields['region'].queryset = Region.objects.filter(country_id=country).order_by('name')
            self.fields['city'].queryset = City.objects.filter(region_id=region).order_by('name')


    class Meta:
        model = Addresses
        fields = ('country', 'region', 'city', 'zipcode', 'address', 'neighborhood', 'number',)


class UserForm(forms.ModelForm):
    document_1 = forms.CharField(label=_("Fiscal document"))
    document_2 = forms.CharField(label=_("Registration document"))
    mobile_phone = forms.CharField(label=_("Mobile phone"))

    class Meta:
        model = Users
        fields = ('first_name', 'last_name', 'email', 'document_1', 'document_2', 'mobile_phone')


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
        fields = ('bank', 'agency', 'agency_digit', 'account_type', 'account_number', 'account_number_digit',)


class ChangePasswordForm(forms.Form):
    form_name = forms.CharField(widget=forms.HiddenInput(), initial='change_password')
    password = PasswordField(label=_("New password"), strip=settings.ACCOUNT_PASSWORD_STRIP)
    repeat_password = forms.CharField(label=_("Repeat password"), widget=forms.PasswordInput())
    current_password = forms.CharField(label=_("Current password"), widget=forms.PasswordInput())

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