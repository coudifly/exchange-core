from exchange_core.models import Users, Currencies, Accounts
from exchange_core.choices import ACTIVE_STATE
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required

import graphene
import graphql_jwt



class User(DjangoObjectType):
    class Meta:
        model = Users


class Currency(DjangoObjectType):
    class Meta:
        model = Currencies


class Account(DjangoObjectType):
    class Meta:
        model = Accounts


class Query(graphene.ObjectType):
    me = graphene.Field(User)
    currency = graphene.List(Currency)
    account = graphene.List(Account)

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


class Auth(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Auth)