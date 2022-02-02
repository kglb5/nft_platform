from patreon.constants.paypal_api_constants import *
from patreon.exception.payment_errors import PendingPaypalTransaction
from patreon.services.payment_apis.external_payment_api_resources import PaypalResource, StripeResource


class ChargeResource:
    @property
    def transaction_id(self):
        raise NotImplemented

    @property
    def fee_amount_cents(self):
        raise NotImplemented

    def __iter__(self):
        yield self.transaction_id
        yield self.fee_amount_cents


class PaypalChargeResource(PaypalResource, ChargeResource):
    @property
    def transaction_id(self):
        return self._get_data_member(TRANSACTION_ID_KEY)

    @property
    def fee_amount_cents(self):
        if self._get_data_member(PAYMENT_STATUS_KEY) == 'Pending':
            raise PendingPaypalTransaction(
                self._get_data_member(RESPONSE_BODY_KEY_LONG) or self._get_data_member(RESPONSE_BODY_KEY),
                self._get_data_member(TRANSACTION_ID_KEY),
                None,
                None)
        return self._get_data_member(FEE_AMOUNT_KEY, 0) * 100


class StripeChargeResource(StripeResource, ChargeResource):
    @property
    def transaction_id(self):
        return self._get_data_member('id')

    @property
    def fee_amount_cents(self):
        return self._get_data_member('fee')
