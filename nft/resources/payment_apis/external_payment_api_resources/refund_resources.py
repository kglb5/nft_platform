from patreon.constants.paypal_api_constants import *
from patreon.services.payment_apis.external_payment_api_resources import PaypalResource, StripeResource


class RefundResource:
    @property
    def refund_id(self):
        raise NotImplemented

    @property
    def gross_refund_amount(self):
        raise NotImplemented

    def __iter__(self):
        yield self.refund_id
        yield self.gross_refund_amount


class PaypalRefundResource(PaypalResource, RefundResource):
    @property
    def refund_id(self):
        return self._get_data_member(REFUND_TRANSACTION_KEY)

    @property
    def gross_refund_amount(self):
        return self._get_data_member(REFUND_AMOUNT_KEY)


class StripeRefundResource(StripeResource, RefundResource):
    @property
    def refund_id(self):
        return self._get_data_member('id')

    @property
    def gross_refund_amount(self):
        return self._get_data_member('amount')
