from django.contrib import admin, messages
from django.utils.translation import ugettext_lazy as _
from django.db import transaction

from exchange_core.models import Users, Companies, Currencies, Accounts, Documents, BankWithdraw, CryptoWithdraw, Statement


class BaseAdmin(admin.ModelAdmin):
    list_per_page = 50

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def log_addition(self, *args, **kwargs):
        pass

    def log_change(self, *args, **kwargs):
        pass

    def log_deletion(self, *args, **kwargs):
        pass


def approve_documents(modeladmin, request, queryset):
    with transaction.atomic():
        queryset.update(status=Users.STATUS.approved_documentation)
    messages.success(request, _("Documentation approved for users"))


approve_documents.short_description = _(
    "Approve documentation for selected users")


def disapprove_documents(modeladmin, request, queryset):
    with transaction.atomic():
        queryset.update(status=Users.STATUS.disapproved_documentation)
    messages.success(request, _("Documentation disapproved for users"))


disapprove_documents.short_description = _(
    "Disapprove documentation for selected users")


@admin.register(Users)
class UsersAdmin(BaseAdmin):
    list_display = ['username', 'first_name', 'last_name', 'email', 'created']
    list_filter = ['status', 'type']
    search_fields = ['username', 'email', 'document_1', 'document_2']
    ordering = ('-created',)
    exclude = ['password']
    readonly_fields = ['last_login', 'profile', 'status', ]
    actions = [approve_documents, disapprove_documents]


@admin.register(Companies)
class CompaniesAdmin(BaseAdmin):
    list_display = ['user', 'name', 'document_1', 'document_2']


@admin.register(Currencies)
class CurrenciesAdmin(BaseAdmin):
    list_display = ['name', 'code', 'type', 'icon', 'withdraw_min',
                    'withdraw_max', 'withdraw_fee', 'withdraw_fixed_fee', 'withdraw_receive_hours']


@admin.register(Accounts)
class AccountsAdmin(BaseAdmin):
    list_display = ['user', 'currency', 'balance', 'deposit', 'reserved']
    search_fields = ['user__username', 'user__email']


@admin.register(Documents)
class DocumentsAdmin(BaseAdmin):
    list_display = ['user', 'file', 'type',
                    'get_document_1', 'get_document_2', 'status']
    list_filter = ['type', 'status']
    search_fields = ['user__username', 'user__email',
                     'user__document_1', 'user__document_2']

    def get_document_1(self, obj):
        return obj.user.document_1

    get_document_1.short_description = _("CPF")
    get_document_1.admin_order_field = 'user__document_1'

    def get_document_2(self, obj):
        return obj.user.document_2

    get_document_2.short_description = _("RG")
    get_document_2.admin_order_field = 'user__document_2'


@admin.register(BankWithdraw)
class BankWithdrawAdmin(BaseAdmin):
    list_display = ['get_user', 'get_document_1', 'get_document_2', 'bank', 'agency', 'agency_digit',
                    'account_type', 'account_number', 'account_number_digit', 'amount', 'fee', 'status']
    list_filter = ['status']
    search_fields = ['account__user__username', 'account__user__email',
                     'account__user__document_1', 'account_user__document_2']
    readonly_fields = ['account']

    def get_user(self, obj):
        return obj.account.user.username

    get_user.short_description = _("Username")
    get_user.admin_order_field = _("account__user__username")

    def get_document_1(self, obj):
        return obj.account.user.document_1

    get_document_1.short_description = _("CPF")
    get_document_1.admin_order_field = "user__document_1"

    def get_document_2(self, obj):
        return obj.account.user.document_2

    get_document_2.short_description = _("RG")
    get_document_2.admin_order_field = "user__document_2"


def reverse_crypto_withdraw(modeladmin, request, queryset):
    with transaction.atomic():
        for crypto_withdraw in queryset.select_related('account__user', 'account__currency'):
            with transaction.atomic():
                if crypto_withdraw.status == CryptoWithdraw.STATUS.reversed:
                    print('1')
                    continue

                if Statement.objects.filter(fk=crypto_withdraw.code, type=Statement.TYPES.reverse).exists():
                    print('2')
                    continue

                account = crypto_withdraw.account
                account.deposit += abs(crypto_withdraw.amount)
                account.save()

                statement = Statement()
                statement.account = account
                statement.type = Statement.TYPES.reverse
                statement.description = "Reverse"
                statement.amount = abs(crypto_withdraw.amount)
                statement.fk = crypto_withdraw.code
                statement.save()

                crypto_withdraw.status = CryptoWithdraw.STATUS.reversed
                crypto_withdraw.save()

                messages.success(request, _("{} amount reversed to {}").format(
                    abs(crypto_withdraw.amount), account.user.username))


reverse_crypto_withdraw.short_description = _(
    "Reverse selected crypto withdraw")


@admin.register(CryptoWithdraw)
class CryptoWithdrawAdmin(BaseAdmin):
    list_display = ['get_user', 'get_document_1', 'get_document_2',
                    'deposit', 'reserved', 'get_coin', 'amount', 'fee', 'status']
    list_filter = ['status']
    search_fields = ['account__user__username', 'account__user__email',
                     'account__user__document_1', 'account_user__document_2']
    actions = [reverse_crypto_withdraw]
    readonly_fields = ['account', 'status']

    def get_coin(self, obj):
        return obj.account.currency.name

    get_coin.short_description = _("Currency")
    get_coin.admin_order_field = "account__currency__name"

    def get_user(self, obj):
        return obj.account.user.username

    get_user.short_description = _("Username")
    get_user.admin_order_field = "account__user__username"

    def get_document_1(self, obj):
        return obj.account.user.document_1

    get_document_1.short_description = _("CPF")
    get_document_1.admin_order_field = "user__document_1"

    def get_document_2(self, obj):
        return obj.account.user.document_2

    get_document_2.short_description = _("RG")
    get_document_2.admin_order_field = "user__document_2"


@admin.register(Statement)
class StatementAdmin(BaseAdmin):
    list_display = ['get_user', 'get_name', 'get_document_1', 'get_document_2',
                    'description', 'amount', 'fk', 'tx_id', 'created']
    list_filter = ['type']
    search_fields = ['description', 'type',]
    readonly_fields = ['account', 'type', 'fk', 'tx_id']

    def has_delete_permission(self, request, obj=None):
        return True

    def get_coin(self, obj):
        return obj.account.currency.name

    get_coin.short_description = _("Currency")
    get_coin.admin_order_field = "account__currency__name"

    def get_user(self, obj):
        return obj.account.user.username

    def get_name(self, obj):
        return obj.account.user.get_full_name()

    get_name.short_description = _("Name")
    get_name.admin_order_field = "account__user__first_name"

    def get_document_1(self, obj):
        return obj.account.user.document_1

    get_document_1.short_description = _("CPF")
    get_document_1.admin_order_field = "user__document_1"

    def get_document_2(self, obj):
        return obj.account.user.document_2

    get_document_2.short_description = _("RG")
    get_document_2.admin_order_field = "user__document_2"
