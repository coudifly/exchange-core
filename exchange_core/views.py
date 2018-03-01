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
from django.utils.text import slugify
from account.decorators import login_required
from account.models import EmailAddress
from account.hooks import hookset

import account.views

from exchange_core.base_views import MultiFormView
from exchange_core import forms
from exchange_core.models import Users, Accounts, BankAccounts, Documents, Statement, CryptoWithdraw, BankWithdraw


class HomeView(TemplateView):
    def get(self, request):
        return redirect('two_factor:login')


class SignupView(account.views.SignupView):
    form_class = forms.SignupForm

    # Sobreescreve o metodo after_signup para popular campos adicionais do usuário
    def after_signup(self, form):
        user = self.created_user
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.document_1 = form.cleaned_data['document_1']
        user.document_2 = form.cleaned_data['document_2']
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
            icon = account.currency.icon.url if account.currency.icon else None

            wallets.append({
                'pk': account.pk,
                'icon': icon,
                'name': account.currency.name,
                'slug': slugify(account.currency.name),
                'symbol': account.currency.symbol,
                'deposit': account.deposit,
                'reserved': account.reserved,
                'withdraw_min': account.currency.withdraw_min,
                'withdraw_max': account.currency.withdraw_max,
                'withdraw_fee': account.currency.withdraw_fee,
                'withdraw_receive_hours': account.currency.withdraw_receive_hours
            })

        return render(request, self.template_name, {'wallets': list(wallets)})


@method_decorator([login_required], name='dispatch')
class AccountSettingsView(MultiFormView):
    template_name = 'account/settings.html'

    forms = {
        'bank_account': forms.BankAccountForm,
        'avatar': forms.AvatarForm,
        'change_password': forms.ChangePasswordForm
    }

    pass_user = [
        'change_password'
    ]

    def get_bank_account_instance(self):
        bank_accounts = BankAccounts.objects.filter(account__currency__symbol=settings.BRL_CURRENCY_SYMBOL, account__user=self.request.user)
        if bank_accounts.exists():
            return bank_accounts.first()

    def bank_account_form_valid(self, form):
        account = Accounts.objects.get(currency__symbol=settings.BRL_CURRENCY_SYMBOL, user=self.request.user)
        bank_account = form.save(commit=False)
        bank_account.account = account
        bank_account.save()

        messages.success(self.request, _('Your bank account settings has been updated'))
        return redirect(reverse('core>settings'))

    def get_avatar_instance(self):
        return self.request.user

    def avatar_form_valid(self, form):
        form.save()

        messages.success(self.request, _('Your avatar image has been updated'))
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
        'contract': forms.DocumentForm,
        'id_front': forms.DocumentForm,
        'id_back': forms.DocumentForm,
        'selfie': forms.DocumentForm
    }

    def get_instance(self, type_name):
        documents = Documents.objects.filter(user=self.request.user, type=type_name)

        if documents.exists():
            return documents.first()

    def form_valid(self, form, type_name):
        instance = form.save(commit=False)
        instance.type = type_name
        instance.user = self.request.user
        instance.save()

        messages.success(self.request, _("Document has been updated!"))
        return redirect(reverse('core>documents'))


@method_decorator([login_required], name='dispatch')
class StatementView(TemplateView):
    template_name = 'core/statement.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['statement'] = Statement.objects.filter(account__user=self.request.user)
        context['crypto_withdraw'] = CryptoWithdraw.objects.filter(account__user=self.request.user)
        context['bank_withdraw'] = BankWithdraw.objects.filter(account__user=self.request.user)
        return context