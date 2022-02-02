import datetime

from patreon.constants.cards import PAYPAL, OTHER, names_to_types
from patreon.constants.paypal_api_constants import *
from patreon.services.payment_apis.external_payment_api_resources import PaypalResource


class CardResource:
    @property
    def card_id(self):
        raise NotImplemented

    @property
    def last_4(self):
        raise NotImplemented

    @property
    def type(self):
        raise NotImplemented

    @property
    def country(self):
        raise NotImplemented

    @property
    def expiration(self):
        raise NotImplemented

    def __iter__(self):
        yield self.card_id
        yield self.last_4
        yield self.type
        yield self.country
        yield self.expiration


class PaypalCardResource(PaypalResource, CardResource):
    @property
    def card_id(self):
        return self._get_data_member(BILLING_AGREEMENT_KEY)

    @property
    def last_4(self):
        return None

    @property
    def type(self):
        return PAYPAL

    @property
    def country(self):
        return None

    @property
    def expiration(self):
        return None


class StripeCardResource(PaypalResource, CardResource):
    @property
    def __stripe_card(self):
        return self._get_data_member('active_card')

    @property
    def card_id(self):
        return self._get_data_member('id')

    @property
    def last_4(self):
        return self.__stripe_card.get('last4')

    @property
    def type(self):
        return names_to_types.get(self.__stripe_card.get('type'), OTHER)

    @property
    def country(self):
        return self.__stripe_card.get('country')

    @property
    def expiration(self):
        month, year = self.__stripe_card.get('exp_month'), self.__stripe_card.get('exp_year')
        return datetime.datetime(year=year, month=month, day=1)
