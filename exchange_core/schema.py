from django.contrib.gis.db.models import PointField
from cities.models import Country as Countries, Region as States, City as Cities
from graphene_django import DjangoObjectType
from graphene_django.converter import convert_django_field
from graphql_jwt.decorators import login_required

from exchange_core.models import Users, Currencies, Accounts, Addresses, BankWithdraw, CryptoWithdraw, Statement
from exchange_core.choices import ACTIVE_STATE
from exchange_orderbook.models import BaseCurrencies, CurrencyPairs, Orders

import graphene
import graphql_jwt


@convert_django_field.register(PointField)
def convert_field_to_int(field, registry=None):
    return graphene.String(description=field.help_text, required=not field.null)


class User(DjangoObjectType):
    class Meta:
        model = Users


class Currency(DjangoObjectType):
    class Meta:
        model = Currencies


class Account(DjangoObjectType):
    class Meta:
        model = Accounts


class Address(DjangoObjectType):
    class Meta:
        model = Addresses


class BankWithdrawal(DjangoObjectType):
    class Meta:
        model = BankWithdraw


class CryptoWithdrawal(DjangoObjectType):
    class Meta:
        model = CryptoWithdraw


class Report(DjangoObjectType):
    class Meta:
        model = Statement


class Contry(DjangoObjectType):
    class Meta:
        model = Countries


class State(DjangoObjectType):
    class Meta:
        model = States


class City(DjangoObjectType):
    class Meta:
        model = Cities


class BaseCurrency(DjangoObjectType):
    class Meta:
        model = BaseCurrencies


class CurrencyPair(DjangoObjectType):
    class Meta:
        model = CurrencyPairs


class Order(DjangoObjectType):
    class Meta:
        model = Orders


class Query(graphene.ObjectType):
    me = graphene.Field(User)
    currency = graphene.List(Currency)
    account = graphene.List(Account)
    address = graphene.List(Address)
    bank_withdrawal = graphene.List(BankWithdrawal)
    crypto_withdrawal = graphene.List(CryptoWithdrawal)
    statement = graphene.List(Report)
    country = graphene.List(Contry)
    state = graphene.List(State)
    city = graphene.List(City)
    base_currency = graphene.List(BaseCurrency)
    currency_pair = graphene.List(CurrencyPair)
    order = graphene.List(Order)


    @login_required
    def resolve_me(self, info):
        return Users.objects.get(pk=info.context.user.pk)

    @login_required
    def resolve_currency(self, info):
        return Currencies.objects.filter(state=ACTIVE_STATE)

    @login_required
    def resolve_account(self, info):
        user = info.context.user
        return Accounts.objects.filter(user=user)

    @login_required
    def resolve_address(self, info):
        user = info.context.user
        return Addresses.objects.filter(user=user)

    @login_required
    def resolve_bank_withdrawal(self, info):
        user = info.context.user
        return BankWithdraw.objects.filter(account__user=user)

    @login_required
    def resolve_crypto_withdrawal(self, info):
        user = info.context.user
        return CryptoWithdraw.objects.filter(account__user=user)

    @login_required
    def resolve_statement(self, info):
        user = info.context.user
        return Statement.objects.filter(account__user=user)

    def resolve_country(self, info):
        return Countries.objects.all()

    def resolve_state(self, info):
        return States.objects.all()

    def resolve_city(self, info):
        return Cities.objects.all()

    def resolve_base_currency(self, info):
        return BaseCurrencies.objects.all()

    def resolve_currency_pair(self, info):
        return CurrencyPairs.objects.all()

    @login_required
    def resolve_order(self, info):
        user = info.context.user
        return Orders.objects.filter(user=user)


class Auth(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Auth)