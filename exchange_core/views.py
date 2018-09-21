import uuid

from django.contrib.auth import get_user_model
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.generic import View, TemplateView
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from django.utils.text import slugify
from django.db import transaction
from jsonview.decorators import json_view
from account.decorators import login_required
from account.models import EmailAddress
from account.hooks import hookset

import account.views

from exchange_core.base_views import MultiFormView
from exchange_core import forms
from exchange_core.models import Users, Accounts, BankAccounts, Documents, Statement, CryptoWithdraw, BankWithdraw, Addresses
from exchange_core.pagination import paginate
from exchange_core.response import JsonResponse
from exchange_core.choices import ACTIVE_STATE

from cities.models import Region, City

try:
    from exchange_orderbook.models import Orders
    from exchange_orderbook.choices import EXECUTED_STATE
    ORDER_EXCHANGE_MODULE_EXISTS = True
except (ImportError, RuntimeError):
    ORDER_EXCHANGE_MODULE_EXISTS = False


class HomeView(TemplateView):
    def get(self, request):
        return redirect(settings.HOME_VIEW)


class SignupView(account.views.SignupView):
    form_class = forms.SignupForm

    def proccess_address_form(self):
        if not getattr(self, '_use_address', True):
            return
        form = forms.AddressForm(country=None, region=None)
        if self.request.method == 'POST':
            country = self.request.POST['country']
            region = self.request.POST['region']
            form = forms.AddressForm(
                self.request.POST, country=country, region=region)
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_address'] = self.proccess_address_form()
        return context

    def form_valid(self, *args, **kwargs):
        form_address = self.proccess_address_form()
        if form_address and not form_address.is_valid():
            return render(self.request, self.template_name, self.get_context_data())
        self.form_address = form_address

        with transaction.atomic():
            return super().form_valid(*args, **kwargs)

    # Sobreescreve o metodo after_signup para popular campos adicionais do usuário
    def after_signup(self, form):
        user = self.created_user
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.document_1 = form.cleaned_data['document_1']
        user.document_2 = form.cleaned_data['document_2']
        user.mobile_phone = form.cleaned_data['mobile_phone']
        user.save()

        form_address = self.form_address.save(commit=False)
        form_address.user = user
        form_address.save()


class ResendConfirmationEmailView(account.views.SignupView):
    def post(self, request):
        email_address = get_object_or_404(
            EmailAddress, email=request.POST['email'], verified=False)
        email_address.send_confirmation(site=get_current_site(self.request))
        messages.success(request, _("Confirmation e-mail resent!"))
        self.created_user = email_address.user
        return self.email_confirmation_required_response()


class ResetPasswordView(account.views.PasswordResetView):
    def send_email(self, email):
        User = get_user_model()
        protocol = getattr(settings, "DEFAULT_HTTP_PROTOCOL", "http")
        current_site = get_current_site(self.request)
        email_qs = EmailAddress.objects.filter(email__iexact=email)

        for user in User.objects.filter(pk__in=email_qs.values("user")):
            token = self.make_token(user)
            password_reset_url = "{0}://{1}{2}".format(
                protocol,
                current_site.domain,
                reverse("core>reset-token",
                        kwargs=dict(uidb36=str(user.pk), token=token))
            )
            hookset.send_password_reset_email([user.email], {
                "user": user,
                "current_site": current_site,
                "password_reset_url": password_reset_url,
            })


class ResetTokenView(account.views.PasswordResetTokenView):
    form_class = forms.ResetTokenForm

    def get_user(self):
        uid_int = self.kwargs["uidb36"]
        return get_object_or_404(get_user_model(), id=uuid.UUID(uid_int))

    def form_valid(self, form):
        self.change_password(form)
        self.create_password_history(form, self.get_user())
        self.after_change_password()
        return redirect(self.get_success_url())


@method_decorator([login_required], name='dispatch')
class WalletsView(TemplateView):
    template_name = 'core/wallets.html'


@method_decorator([login_required], name='dispatch')
class GetWalletsView(View):
    def get(self, request):
        wallets = []

        for account in Accounts.objects.select_related('currency').filter(user=request.user, currency__state=ACTIVE_STATE):
            icon = account.currency.icon.url if account.currency.icon else None

            wallets.append({
                'pk': account.pk,
                'icon': icon,
                'name': account.currency.name,
                'slug': slugify(account.currency.name),
                'code': account.currency.code,
                'deposit': account.deposit,
                'reserved': account.reserved,
                'balance': account.balance,
                'withdraw_min': account.currency.withdraw_min,
                'withdraw_max': account.currency.withdraw_max,
                'withdraw_fee': account.currency.withdraw_fee,
                'withdraw_fixed_fee': account.currency.withdraw_fixed_fee,
                'withdraw_receive_hours': account.currency.withdraw_receive_hours
            })

        return JsonResponse({'wallets': wallets})


@method_decorator([login_required], name='dispatch')
class AccountSettingsView(MultiFormView):
    template_name = 'account/settings.html'

    forms = {
        'bank_account': forms.BankAccountForm,
        'user': forms.UserForm,
        'address': forms.AddressForm,
        'avatar': forms.AvatarForm,
        'change_password': forms.ChangePasswordForm
    }

    pass_user = [
        'change_password',
        'user',
    ]

    def get_bank_account_instance(self):
        bank_accounts = BankAccounts.objects.filter(
            account__currency__code=settings.BRL_CURRENCY_SYMBOL, account__user=self.request.user)
        if bank_accounts.exists():
            return bank_accounts.first()

    def bank_account_form_valid(self, form):
        account = Accounts.objects.get(
            currency__code=settings.BRL_CURRENCY_SYMBOL, user=self.request.user)
        bank_account = form.save(commit=False)
        bank_account.account = account
        bank_account.save()

        messages.success(self.request, _('Your bank account settings has been updated'))
        return redirect(reverse('core>settings'))

    def get_address_kwargs(self):
        country = self.request.POST.get('country')
        region = self.request.POST.get('region')
        return {'country': country, 'region': region}

    def get_address_instance(self):
        addresses = Addresses.objects.filter(user=self.request.user)
        if addresses.exists():
            return addresses.first()

    def get_avatar_instance(self):
        return self.request.user

    def get_user_instance(self):
        return self.request.user

    def avatar_form_valid(self, form):
        form.save()
        messages.success(self.request, _('Your avatar image has been updated'))
        return redirect(reverse('core>settings'))

    def address_form_valid(self, form):
        with transaction.atomic():
            instance = form.save(commit=False)
            instance.user = self.request.user
            instance.save()
            user = instance.user
            user.profile['has_address'] = True
            user.save()

        messages.success(self.request, _('Your address has been updated'))
        return redirect(reverse('core>settings'))

    def user_form_valid(self, form):
        instance = form.save(commit=False)
        instance.profile['has_personal'] = True
        instance.save()
        messages.success(self.request, _(
            'Your personal data has been updated'))
        return redirect(reverse('core>settings'))

    def change_password_form_valid(self, form):
        user = self.request.user
        user.set_password(form.cleaned_data['password'])
        user.save()
        messages.success(self.request, _('Your password has been updated'))
        return redirect(reverse('two_factor:login'))


@method_decorator([login_required], name='dispatch')
class DocumentsView(MultiFormView):
    template_name = 'core/documents.html'

    forms = {
        'id_front': forms.DocumentForm,
        'id_back': forms.DocumentForm,
        'selfie': forms.DocumentForm,
        'contract': forms.DocumentForm,
        'residence': forms.DocumentForm
    }

    def get_instance(self, type_name):
        documents = Documents.objects.select_related(
            'user').filter(user=self.request.user, type=type_name)
        if documents.exists():
            return documents.first()

    def form_valid(self, form, type_name):
        with transaction.atomic():
            instance = form.save(commit=False)
            instance.type = type_name
            instance.user = self.request.user
            instance.status = Documents.STATUS.pending
            instance.save()

            user = self.request.user

            if user.status == Users.STATUS.disapproved_documentation:
                user.status = Users.STATUS.created
                user.save()

            messages.success(self.request, _("Document has been updated!"))
        return redirect(reverse('core>documents'))


@method_decorator([login_required], name='dispatch')
class StatementView(TemplateView):
    template_name = 'core/statement.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['statement'] = paginate(self.request, Statement.objects.filter(account__user=self.request.user, type__in=[
                                        'deposit', 'withdraw', 'reverse']).order_by('-created'), url_param_name='statement_page')
        context['bank_withdraw'] = paginate(self.request, BankWithdraw.objects.filter(
            account__user=self.request.user).order_by('-created'), url_param_name='bank_withdraw_page')
        context['crypto_withdraw'] = paginate(self.request, CryptoWithdraw.objects.filter(
            account__user=self.request.user).order_by('-created'), url_param_name='crypto_withdraw_page')

        if ORDER_EXCHANGE_MODULE_EXISTS:
            context['executed_orders'] = Orders.objects.select_related('currency_pair__base_currency__currency', 'currency_pair__quote_currency').filter(
                user=self.request.user, state=EXECUTED_STATE).order_by('-created')[0:50]

        return context


@method_decorator([json_view], name='dispatch')
class GetRegionsView(View):
    def get(self, request):
        country = request.GET.get(
            'country', settings.DEFAULT_ADDRESS_COUNTRY).replace('.', '')
        regions = [{'pk': '', 'name': _("-- Select your region --")}]

        for region in Region.objects.filter(country_id=country).order_by('name'):
            regions.append({'pk': region.pk, 'name': region.name})

        return regions


@method_decorator([json_view], name='dispatch')
class GetCitiesView(View):
    def get(self, request):
        region = request.GET.get('region', 3390290).replace('.', '')
        cities = [{'pk': '', 'name': _("-- Select your city --")}]

        for city in City.objects.filter(region_id=region).order_by('name'):
            cities.append({'pk': city.pk, 'name': city.name})

        return cities
