import uuid

from django.contrib.auth import get_user_model
from django.contrib import messages
from django.views.generic.edit import FormView
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from account.decorators import login_required
from account.models import EmailAddress
from account.hooks import hookset

import account.views

from . import forms
from .models import Users, Accounts, BankAccounts


class MultiFormView(TemplateView):
    forms = {}

    def get_context_data(self):
        context = super().get_context_data()
        for alias, form in self.forms.items():
            kwargs = self.get_kwargs(alias)
            context['form_' + alias] = form(**kwargs)
        return context

    def get_kwargs(self, alias):
        kwargs = {}
        instance_method = self.get_method('get_{}_instance'.format(alias))
        if instance_method:
            kwargs = {'instance': instance_method()}
        return kwargs

    def get_current_form(self):
        self.alias = self.request.POST['form_alias']
        return self.forms[self.alias]

    def get_method(self, method_name):
        if hasattr(self, method_name):
            method = getattr(self, method_name)
            return method

    def get(self, request):
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def post(self, request):
        current_form = self.get_current_form()
        kwargs = self.get_kwargs(self.alias)
        form = current_form(request.POST, request.FILES, **kwargs)

        if form.is_valid():
            form_valid_method = self.get_method('{}_form_valid'.format(self.alias))
            return form_valid_method(form)

        context = self.get_context_data()
        context['form_' + self.alias] = form
        return render(request, self.template_name, context)


class SignupView(account.views.SignupView):
    form_class = forms.SignupForm

    # Sobreescreve o metodo after_signup para popular campos adicionais do usuário
    def after_signup(self, form):
        user = self.created_user
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.save()


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
                reverse("core>reset-token", kwargs=dict(uidb36=str(user.pk), token=token))
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

    def get(self, request):
        wallets = []

        for account in Accounts.objects.filter(user=request.user):
            wallets.append({
                'pk': account.pk,
                'icon': account.currency.icon.url,
                'name': account.currency.name,
                'symbol': account.currency.symbol,
                'deposit': account.deposit,
                'reserved': account.reserved
            })

        return render(request, self.template_name, {'wallets': list(wallets)})


@method_decorator([login_required], name='dispatch')
class AccountSettingsView(MultiFormView):
    template_name = 'account/settings.html'

    forms = {
        'settings': forms.AccountSettingsForm,
        'avatar': forms.AvatarForm,
        'bank_account': forms.BankAccountForm
    }

    def get_bank_account_instance(self):
        bank_accounts = BankAccounts.objects.filter(account__currency__symbol=settings.BRL_CURRENCY_SYMBOL, account__user=self.request.user)
        if bank_accounts.exists():
            return bank_accounts.first()

    def bank_account_form_valid(self, form):
        account = Accounts.objects.get(currency__symbol=settings.BRL_CURRENCY_SYMBOL, user=self.request.user)
        bank_account = form.save(commit=False)
        bank_account.account = account
        bank_account.save()

        messages.success(self.request, _('Your bank account settings were updated'))

        return redirect(reverse('core>settings'))


@method_decorator([login_required], name='dispatch')
class AvatarView(TemplateView):
    def post(self, request):
        avatar_form = forms.AvatarForm(request.POST, request.FILES, instance=request.user)
        if avatar_form.is_valid():
            avatar_form.save()
        return redirect(reverse('core>settings'))
