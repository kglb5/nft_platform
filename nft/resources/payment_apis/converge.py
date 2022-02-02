import stripe
from functools import wraps

import patreon
from patreon.exception.generic_errors import TestEnvironmentOnly
from patreon.exception.payment_errors import *
from patreon.services.payment_apis import ExternalPaymentAPIInterface, capture_external_payment_api_exception_events
from patreon.services.payment_apis.external_payment_api_resources import StripeChargeResource, StripeRefundResource, \
    StripeCardResource, StripeTransactionResource
from patreon.util import function_tools


def _construct_exception_arguments(exception, kwargs):
    return {
        'exception': exception,
        'transaction_id': kwargs.get('transaction_id'),
        'instrument_id': kwargs.get('instrument_id'),
        'amount_cents': kwargs.get('amount_cents')
    }


def _normalize_exceptions(inner_f):
    """
    Reraise stripe exceptions as exceptions understood by the payments_mgr
    """

    @wraps(inner_f)
    @capture_external_payment_api_exception_events
    def create_wrapper(*args, **kwargs):
        kwargs.update(function_tools.convert_args_to_kwargs(inner_f, args))
        try:
            return inner_f(**kwargs)

        except stripe.error.CardError as exception:
            # Since it's a decline, stripe.error.CardError will be caught

            arguments = _construct_exception_arguments(exception, kwargs)
            raise CardDeclineError(**arguments)

        except stripe.error.InvalidRequestError as exception:
            # Invalid parameters were supplied to Stripe's API

            arguments = _construct_exception_arguments(exception, kwargs)

            if 'Keys for idempotent requests can only be used' in str(exception):
                raise ReusedIdempotencyKey(**arguments)
            raise InvalidAPIRequest(**arguments)

        except stripe.error.AuthenticationError as exception:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)

            arguments = _construct_exception_arguments(exception, kwargs)
            raise AuthenticationError(**arguments)

        except stripe.error.APIConnectionError as exception:
            # Network communication with Stripe failed

            arguments = _construct_exception_arguments(exception, kwargs)
            raise TemporaryOutage(**arguments)

        except stripe.error.StripeError as exception:
            # Display a very generic error to the user, and maybe send
            # yourself an email

            arguments = _construct_exception_arguments(exception, kwargs)
            raise TemporaryOutage(**arguments)

        except ExternalPaymentAPIException as exception:
            raise exception

        except Exception as exception:
            # Something else happened, completely unrelated to Stripe
            arguments = _construct_exception_arguments(exception, kwargs)
            raise GenericCodeFailure(**arguments)

    return create_wrapper


class StripeAPI(ExternalPaymentAPIInterface):
    def __init__(self):

        try:
            _ = patreon.config.stripe
        except Exception as exception:
            raise ConfigError(exception)

        try:
            stripe.api_key = patreon.config.stripe['secret_key']
        except Exception as exception:
            raise ConfigError(exception)

    def __get_transaction_by_id(self, transaction_id):
        return stripe.Charge.retrieve(transaction_id)

    @_normalize_exceptions
    def charge_instrument(self, payment_id, instrument_id, amount_cents, description=None):
        result = stripe.Charge.create(
            amount=amount_cents,
            currency="usd",
            customer=instrument_id,
            description=description,
            idempotency_key=payment_id
        )
        # TODO Log this to redshift
        return StripeChargeResource(result)

    @_normalize_exceptions
    def get_transaction_status(self, transaction_id):
        # todo return in single format across all payment methods
        # TODO Log this to redshift
        return StripeTransactionResource(self.__get_transaction_by_id(transaction_id))

    @_normalize_exceptions
    def refund_transaction(self, refund_id, transaction_id):
        charge = self.__get_transaction_by_id(transaction_id)
        result = charge.refund(idempotency_key=refund_id)
        # TODO Log this to redshift
        return StripeRefundResource(result)

    @_normalize_exceptions
    def refund_transaction_partial(self, refund_id, transaction_id, amount_cents):
        charge = self.__get_transaction_by_id(transaction_id)
        result = charge.refund(amount=amount_cents, idempotency_key=refund_id)
        # TODO Log this to redshift
        return StripeRefundResource(result)

    @_normalize_exceptions
    def add_instrument(self, instrument_token):
        customer = stripe.Customer.create(source=instrument_token)

        return StripeCardResource(customer)

    @_normalize_exceptions
    def get_recent_transactions(self, cursor):
        if cursor:
            return stripe.Charge.all(limit=100, starting_after=cursor)
        return stripe.Charge.all(limit=100)

    @_normalize_exceptions
    def get_test_instrument_id(self, authorization):
        if not patreon.is_test_environment():
            raise TestEnvironmentOnly

        token_resp = stripe.Token.create(
            card=authorization,
        )

        return token_resp['id']

    def raise_generic_api_exception(self, input_exception):
        raise StripeException(input_exception)
