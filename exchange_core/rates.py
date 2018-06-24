from decimal import Decimal

import requests


DEFAULT_CURRENCY = 'BTC'


class CurrencyPrice:
    quote_providers = {}

    def __init__(self, provider, currency=DEFAULT_CURRENCY, amount=1, precision=8):
        if not provider in self.quote_providers:
            raise Exception('{} provider not configured'.format(provider))

        self.provider = self.quote_providers[provider]()
        self.currency = currency
        self.amount = amount
        self.precision = precision

    def get_amount(self, amount):
        if amount is None:
            amount = self.amount
        return amount

    def to_usd(self, amount=None):
        amount = self.get_amount(amount)
        price = self.provider.get_usd_price(self.currency, Decimal(amount))
        return round(price, self.precision)

    def to_br(self, amount=None):
        amount = self.get_amount(amount)
        price = self.provider.get_br_price(self.currency, Decimal(amount))
        return round(price, self.precision)


class CoinBaseProvider:
    name = 'coinbase'
    api = 'https://api.coinbase.com/v2'

    def get(self, path):
        endpoint = '{}{}'.format(self.api, path)
        return requests.get(endpoint).json()

    def get_usd_price(self, currency, amount):
        price = self.get('/prices/spot?currency=USD')
        return Decimal(price['data']['amount']) * amount


class MercadoBitcoinProvider:
    name = 'mercadobitcoin'
    api = 'https://www.mercadobitcoin.net/api'

    def get(self, path):
        endpoint = '{}{}'.format(self.api, path)
        return requests.get(endpoint).json()

    def get_br_price(self, currency, amount):
        price = self.get('/{}/ticker/'.format(currency))
        return Decimal(price['ticker']['last']) * amount


CurrencyPrice.quote_providers[CoinBaseProvider.name] = CoinBaseProvider
CurrencyPrice.quote_providers[MercadoBitcoinProvider.name] = MercadoBitcoinProvider
