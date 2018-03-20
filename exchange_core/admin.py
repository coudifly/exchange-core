from django.contrib import admin, messages
from django.utils.translation import ugettext_lazy as _

from exchange_core.models import Users, Companies, Currencies, Accounts, Documents, BankWithdraw, CryptoWithdraw


def approve_documents(modeladmin, request, queryset):
    with transaction.atomic():
        queryset.update(status=Users.STATUS.approved_documentation)
    messages.success(request, _("Documentation approved for users"))

approve_documents.short_description = _("Approve documentation for selected users")


def disapprove_documents(modeladmin, request, queryset):
    with transaction.atomic():
        queryset.update(status=Users.STATUS.disapproved_documentation)
    messages.success(request, _("Documentation disapproved for users"))

disapprove_documents.short_description = _("Disapprove documentation for selected users")


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ['username', 'sponsor', 'first_name', 'last_name', 'email', 'created']
    list_filter = ['status', 'type']
    search_fields = ['username', 'email', 'document_1', 'document_2']
    ordering = ('-created',)
    actions = [approve_documents, disapprove_documents]


@admin.register(Companies)
class CompaniesAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'document_1', 'document_2']


@admin.register(Currencies)
class CurrenciesAdmin(admin.ModelAdmin):
    list_display = ['name', 'symbol', 'icon', 'withdraw_min', 'withdraw_max', 'withdraw_fee', 'withdraw_receive_hours']


@admin.register(Accounts)
class AccountsAdmin(admin.ModelAdmin):
    list_display = ['user', 'currency', 'balance', 'deposit', 'reserved']
    search_fields = ['user__username', 'user__email']


@admin.register(Documents)
class DocumentsAdmin(admin.ModelAdmin):
    list_display = ['user', 'file', 'type', 'get_document_1', 'get_document_2', 'status']
    list_filter = ['type', 'status']
    search_fields = ['user__username', 'user__email', 'user__document_1', 'user__document_2']

    def get_document_1(self, obj):
        return obj.user.document_1

    get_document_1.short_description = _("CPF")
    get_document_1.admin_order_field = _("user__document_1")

    def get_document_2(self, obj):
        return obj.user.document_2

    get_document_2.short_description = _("RG")
    get_document_2.admin_order_field = _("user__document_2")


@admin.register(BankWithdraw)
class BankWithdrawAdmin(admin.ModelAdmin):
    list_display = ['get_user', 'get_document_1', 'get_document_2', 'bank', 'agency', 'agency_digit', 'account_type', 'account_number', 'account_number_digit', 'amount', 'fee', 'status']
    list_filter = ['status']
    search_fields = ['account__user__username', 'account__user__email', 'account__user__document_1', 'account_user__document_2']

    def get_user(self, obj):
        return obj.account.user.username

    get_user.short_description = _("Username")
    get_user.admin_order_field = _("account__user__username")

    def get_document_1(self, obj):
        return obj.account.user.document_1

    get_document_1.short_description = _("CPF")
    get_document_1.admin_order_field = _("user__document_1")

    def get_document_2(self, obj):
        return obj.account.user.document_2

    get_document_2.short_description = _("RG")
    get_document_2.admin_order_field = _("user__document_2")


def reverse_crypto_withdraw(modeladmin, request, queryset):
    with transaction.atomic():
        for crypto_withdraw in queryset.select_related('account__user', 'account__currency'):
            account = crypto_withdraw.account
            account.deposit += abs(crypto_withdraw.amount)
            account.save()

            statement = Statement()
            statement.account = account
            statement.type = Statement.TYPES.reverse
            statement.description = _("Reverse")
            statement.save()

            crypto_withdraw.status = CryptoWithdraw.STATUS.reversed
            crypto_withdraw.save()

            messages.success(request, _("{} amount reversed to {}").format(abs(crypto_withdraw.amount), account.user.username))

reverse_crypto_withdraw.short_description = _("Reverse selected crypto withdraw")


@admin.register(CryptoWithdraw)
class CryptoWithdrawAdmin(admin.ModelAdmin):
    list_display = ['get_user', 'get_document_1', 'get_document_2', 'deposit', 'reserved', 'get_coin', 'amount', 'fee', 'status']
    list_filter = ['status']
    search_fields = ['account__user__username', 'account__user__email', 'account__user__document_1', 'account_user__document_2']
    actions = [reverse_crypto_withdraw]

    def get_coin(self, obj):
        return obj.account.currency.name

    get_coin.short_description = _("Currency")
    get_coin.admin_order_field = _("account__currency__name")

    def get_user(self, obj):
        return obj.account.user.username

    get_user.short_description = _("Username")
    get_user.admin_order_field = _("account__user__username")

    def get_document_1(self, obj):
        return obj.account.user.document_1

    get_document_1.short_description = _("CPF")
    get_document_1.admin_order_field = _("user__document_1")

    def get_document_2(self, obj):
        return obj.account.user.document_2

    get_document_2.short_description = _("RG")
    get_document_2.admin_order_field = _("user__document_2")