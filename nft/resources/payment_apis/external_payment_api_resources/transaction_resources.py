from patreon.services.payment_apis.external_payment_api_resources import PaypalResource, StripeResource


class TransactionResource:
    @property
    def raw_result(self):
        raise NotImplemented


class PaypalTransactionResource(PaypalResource, TransactionResource):
    @property
    def raw_result(self):
        return self.response_data


class StripeTransactionResource(StripeResource, TransactionResource):
    @property
    def raw_result(self):
        return self.response_data
