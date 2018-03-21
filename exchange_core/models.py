import uuid
from decimal import Decimal

from django.db import models, transaction
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import JSONField
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib import messages
from model_utils.models import TimeStampedModel, StatusModel
from model_utils import Choices
from cities.models import Country, Region, City

from exchange_core.managers import CustomUserManager
from exchange_core.choices import BR_BANKS_CHOICES, BR_ACCOUNT_TYPES_CHOICES


def get_file_path(instance, filename):
    return '{}.{}'.format(uuid.uuid4(), filename.split('.')[-1])


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
       abstract = True


class Users(TimeStampedModel, AbstractUser, BaseModel):
    STATUS = Choices(
                'created', 'approved_documentation',
                'inactive', 'disapproved_documentation'
                )
    TYPES = Choices('person', 'company')

    sponsor = models.ForeignKey('self', null=True, blank=True, verbose_name=_("Sponsor"), on_delete=models.CASCADE)
    status = models.CharField(max_length=30, default=STATUS.created, choices=STATUS, verbose_name=_("Status"))
    avatar = models.ImageField(upload_to=get_file_path, blank=True)
    profile = JSONField(null=True, blank=True, default={})
    type = models.CharField(max_length=11, choices=TYPES, default=TYPES.person, null=True, blank=False)
    document_1 = models.CharField(max_length=50, null=True, blank=True, unique=True)
    document_2 = models.CharField(max_length=50, null=True, blank=True, unique=True)

    objects = CustomUserManager()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._original_status = self.status
        if self.profile is None:
            self.profile = {}

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    # Retorna Yes/No se o usuario tem uma conta bancaria associada a sua conta BRL
    @property
    def has_br_bank_account(self):
        br_account = self.accounts.get(currency__symbol=settings.BRL_CURRENCY_SYMBOL)
        return 'yes' if br_account.bank_accounts.exists() else 'no'

    @property
    def br_bank_account(self):
        br_account = self.accounts.get(currency__symbol=settings.BRL_CURRENCY_SYMBOL)
        if br_account.bank_accounts.exists():
            return br_account.bank_accounts.first()


class Addresses(TimeStampedModel, BaseModel):
    TYPES = Choices('account')

    user = models.ForeignKey(Users, related_name='addresses', on_delete=models.CASCADE)
    country = models.ForeignKey(Country, related_name='addresses', on_delete=models.CASCADE, verbose_name=_("Country"))
    region = models.ForeignKey(Region, related_name='addresses', on_delete=models.CASCADE, verbose_name=_("State"))
    city = models.ForeignKey(City, related_name='addresses', on_delete=models.CASCADE, verbose_name=_("City"))
    address = models.CharField(max_length=100, verbose_name=_("Address"))
    number = models.CharField(max_length=20, verbose_name=_("Number"))
    neighborhood = models.CharField(max_length=50, verbose_name=_("neighborhood"))
    zipcode = models.CharField(max_length=10, verbose_name=_("Zipcode"))
    type = models.CharField(max_length=20, choices=TYPES, default=TYPES.account, verbose_name=_("Type"))


class Companies(TimeStampedModel, BaseModel):
    user = models.ForeignKey(Users, related_name='companies', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    document_1 = models.CharField(max_length=50, null=True, blank=True)
    document_2 = models.CharField(max_length=50, null=True, blank=True)


class Currencies(TimeStampedModel, BaseModel):
    STATUS = Choices('active', 'inactive')
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10, unique=True)
    icon = models.ImageField(upload_to=get_file_path, null=True, blank=True, verbose_name=_("Icon"))
    status = models.CharField(
                            max_length=30, default=STATUS.active,
                            choices=STATUS, verbose_name=_("Status")
                            )
    withdraw_min = models.DecimalField(max_digits=20, decimal_places=8, default=Decimal('0.001'), verbose_name=_("Withdraw Min"))
    withdraw_max = models.DecimalField(max_digits=20, decimal_places=8, default=Decimal('1000000.00'), verbose_name=_("Withdraw Max"))
    withdraw_fee = models.DecimalField(max_digits=20, decimal_places=8, default=Decimal('0.005'), verbose_name=_("Withdraw Percent Fee"))
    withdraw_fixed_fee = models.DecimalField(max_digits=20, decimal_places=8, default=Decimal('0.005'), verbose_name=_("Withdraw Fixed Fee"))
    withdraw_receive_hours = models.IntegerField(default=48)
    order = models.IntegerField(default=100)

    class Meta:
        verbose_name = 'Currency'
        verbose_name_plural = 'Currencies'
        ordering = ['name']

    def __str__(self):
        return self.name


class Accounts(TimeStampedModel, BaseModel):
    currency = models.ForeignKey(Currencies, related_name='accounts', verbose_name=_("Currency"), on_delete=models.CASCADE)
    user = models.ForeignKey(Users, related_name='accounts', null=True, verbose_name=_("User"), on_delete=models.CASCADE)
    deposit = models.DecimalField(max_digits=20, decimal_places=8, default=Decimal('0.00'))
    reserved = models.DecimalField(max_digits=20, decimal_places=8, default=Decimal('0.00'))
    deposit_address = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = 'Currency Account'
        verbose_name_plural = 'Currencies Accounts'
        ordering = ['currency__name']

    def __str__(self):
        return '{} - {}'.format(self.user.username, self.currency.symbol)

    @property
    def balance(self):
        return self.deposit + self.reserved


class BankAccounts(TimeStampedModel, BaseModel):
    bank = models.CharField(max_length=10, choices=BR_BANKS_CHOICES, verbose_name=_("Bank"))
    agency = models.CharField(max_length=10, verbose_name=_("Agency"))
    agency_digit = models.CharField(max_length=5, null=True, verbose_name=_("Digit"))
    account_type = models.CharField(max_length=20, choices=BR_ACCOUNT_TYPES_CHOICES, verbose_name=_("Account type"))
    account_number = models.CharField(max_length=20, verbose_name=_("Account number"))
    account_number_digit = models.CharField(max_length=5, null=True, verbose_name=_("Digit"))
    account = models.ForeignKey(Accounts, related_name='bank_accounts', on_delete=models.CASCADE)


# Base class para saques
class BaseWithdraw(models.Model):
    STATUS = Choices('requested', 'reversed', 'paid')

    deposit = models.DecimalField(max_digits=20, decimal_places=8, default=Decimal('0.00'))
    reserved = models.DecimalField(max_digits=20, decimal_places=8, default=Decimal('0.00'))
    amount = models.DecimalField(max_digits=20, decimal_places=8, default=Decimal('0.00'))
    fee = models.DecimalField(max_digits=20, decimal_places=8, default=Decimal('0.00'))
    status = models.CharField(max_length=20, default=STATUS.requested, choices=STATUS)
    tx_id = models.CharField(max_length=150, null=True, blank=True)

    @property
    def status_name(self):
        return self.status.title()

    @property
    def status_class(self):
        if self.status == self.STATUS.requested:
            return 'warning'
        if self.status == self.STATUS.paid:
            return 'success'
        if self.status == self.STATUS.reversed:
            return 'info'

    # Valor do saque com desconto do fee cobrado
    @property
    def amount_with_discount(self):
        return abs(self.amount) - abs(self.fee)

    class Meta:
        abstract = True


# Saques bancários
class BankWithdraw(TimeStampedModel, BaseWithdraw, BaseModel):
    bank = models.CharField(max_length=10, choices=BR_BANKS_CHOICES)
    agency = models.CharField(max_length=10)
    agency_digit = models.CharField(max_length=5, null=True, verbose_name=_("Agency Digit"))
    account_type = models.CharField(max_length=20, choices=BR_ACCOUNT_TYPES_CHOICES)
    account_number = models.CharField(max_length=20)
    account_number_digit = models.CharField(max_length=5, null=True, verbose_name=_("Account number digit"))
    account = models.ForeignKey(Accounts, related_name='bank_withdraw', on_delete=models.CASCADE)


# Saques de criptomoedas
class CryptoWithdraw(TimeStampedModel, BaseWithdraw):
    address = models.CharField(max_length=255)
    account = models.ForeignKey(Accounts, related_name='crypto_withdraw', on_delete=models.CASCADE)


# Documentos
class Documents(TimeStampedModel, BaseModel):
    TYPES = Choices('id_front', 'id_back', 'selfie', 'contract', 'residence')
    STATUS = Choices('pending', 'disapproved', 'approved')

    user = models.ForeignKey(Users, related_name='documents', on_delete=models.CASCADE)
    file = models.ImageField(upload_to=get_file_path)
    type = models.CharField(max_length=20, choices=TYPES)
    status = models.CharField(max_length=20, choices=STATUS, default=STATUS.pending)
    reason = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("Disapproved reason"))

    class Meta:
        verbose_name = 'Document'
        verbose_name_plural = 'Documents'
        ordering = ['status']

    @property
    def status_title(self):
        return self.status.title()

    # Propriedade para pegar a classe de alerta no template
    @property
    def status_alert_class(self):
        if self.status == self.STATUS.pending:
            return 'alert-warning'
        if self.status == self.STATUS.disapproved:
            return 'alert-danger'
        if self.status == self.STATUS.approved:
            return 'alert-success'


# Extrato das contas
class Statement(TimeStampedModel, BaseModel):
    TYPES = Choices('deposit', 'reverse', 'withdraw', 'income', 'investment')

    account = models.ForeignKey(Accounts, related_name='statement', on_delete=models.CASCADE, verbose_name=_("Account"))
    description = models.CharField(max_length=100, verbose_name=_("Description"))
    amount = models.DecimalField(max_digits=20, decimal_places=8, default=Decimal('0.00'))
    type = models.CharField(max_length=30, choices=TYPES, verbose_name=_("Type"))
    # Campo usado para armazenar o id das transactions e checar se uma transacao ja foi processada ou nao
    tx_id = models.CharField(max_length=150, null=True, blank=True)
    # Chave estrangeira para outro registro
    fk = models.UUIDField(null=True, blank=True, editable=False)

    class Meta:
        verbose_name = _("Statement")
        verbose_name_plural = _("Statement")


# Cria as contas do usuário
@receiver(post_save, sender=Users, dispatch_uid='create_user_accounts')
def create_user_accounts(sender, instance, created, **kwargs):
    if created:
        currencies = Currencies.objects.all()

        with transaction.atomic():
            for currency in currencies:
                account = Accounts()
                account.user = instance
                account.currency = currency
                account.save()


@receiver(post_save, sender=Currencies, dispatch_uid='create_currency_user_accounts')
def create_currency_user_accounts(sender, instance, created, **kwargs):
    with transaction.atomic():
        # Filtra pelos usuários que ainda não tem essa conta
        users = Users.objects.exclude(accounts__currency=instance)

        for user in users:
            account = Accounts()
            account.currency = instance
            account.user = user
            account.save()