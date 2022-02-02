class ExternalPaymentAPIResource:
    def __init__(self, response_data):
        self.response_data = response_data

    def _get_data_member(self, key, *args, **kwargs):
        raise NotImplemented


class PaypalResource(ExternalPaymentAPIResource):
    def _get_data_member(self, key, *args, **kwargs):
        return self.response_data.get(key, *args, **kwargs)

class StripeResource(ExternalPaymentAPIResource):
    def _get_data_member(self, key, *args, **kwargs):
        if not hasattr(self.response_data, key):
            return None

        obj = getattr(self.response_data, key)

        if callable(obj):
            return obj(*args, **kwargs)

        return obj