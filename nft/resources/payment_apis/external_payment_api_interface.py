
class ExternalPaymentAPIInterface:

    def charge_instrument(self, payment_id, instrument_id, amount_cents, description=None):
        raise NotImplemented()

    def get_transaction_status(self, transaction_id):
        raise NotImplemented()

    def refund_transaction(self, refund_id, transaction_id):
        raise NotImplemented()

    def refund_transaction_partial(self, refund_id, transaction_id, amount_cents):
        raise NotImplemented()

    def add_instrument(self, instrument_token):
        raise NotImplemented()

    def get_test_instrument_id(self, authorization):
        raise NotImplemented()
