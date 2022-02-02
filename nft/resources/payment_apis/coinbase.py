import requests
from requests.exceptions import ConnectTimeout, ConnectionError, ReadTimeout
from urllib.parse import unquote
from functools import wraps

import patreon
from patreon.constants import paypal_error_names
from patreon.constants.paypal_api_constants import *
from patreon.exception.generic_errors import TestEnvironmentOnly
from patreon.exception.payment_errors import *
from patreon.services.payment_apis import ExternalPaymentAPIInterface, capture_external_payment_api_exception_events
from patreon.services.payment_apis.external_payment_api_resources import PaypalChargeResource, PaypalRefundResource, \
    PaypalCardResource, PaypalTransactionResource


def _construct_exception_arguments(exception):
    return {
        'exception': exception,
        'transaction_id': exception.transaction_id,
        'instrument_id': exception.instrument_id,
        'amount_cents': exception.amount_cents
    }


def _normalize_exceptions(inner_f):
    @wraps(inner_f)
    @capture_external_payment_api_exception_events
    def create_wrapper(*args, **kwargs):
        try:
            return inner_f(*args, **kwargs)

        except GenericPaypalAPIError as exception:
            arguments = _construct_exception_arguments(exception)

            if exception.message in paypal_error_names.DECLINE_ERRORS:
                raise CardDeclineError(**arguments)

            elif exception.message in paypal_error_names.INVALID_REQUEST:
                raise InvalidAPIRequest(**arguments)

            elif exception.message in paypal_error_names.IDEMPOTENCY_ERROR:
                raise ReusedIdempotencyKey(**arguments)

            elif exception.message in paypal_error_names.TEMPORARY_OUTAGE:
                raise TemporaryOutage(**arguments)

            elif exception.message in paypal_error_names.CONFIG_ERROR:
                raise AuthenticationError(**arguments)

            elif exception.message in paypal_error_names.EMERGENCY_ERRORS:
                raise CardDeclineEmergencyError(**arguments)

            elif exception.message in paypal_error_names.MONTHLY_MAX_ERRORS:
                raise CardDeclineMonthlyMaxError(**arguments)

            elif exception.message in paypal_error_names.FRAUD_ERRORS:
                raise CardDeclineFraudError(**arguments)

            elif exception.message in paypal_error_names.UNKNOWN_ERRORS:
                raise UnexpectedPaypalAPIError(**arguments)

            elif exception.message in paypal_error_names.CANCELED_AGREEMENT:
                raise CancelledBillingAgreement(**arguments)

            raise exception
        except (ConnectionError, TimeoutError, ConnectTimeout, ReadTimeout) as exception:
            raise TemporaryOutage(exception=exception,
                                  transaction_id=kwargs.get('transaction_id'),
                                  instrument_id=kwargs.get('instrument_id'),
                                  amount_cents=kwargs.get('amount_cents'))
        except ExternalPaymentAPIException as e:
            raise e
        except Exception as e:
            raise GenericCodeFailure(e)

    return create_wrapper


class PayPalAPI(ExternalPaymentAPIInterface):
    test_index = 0
    test_keys = ['B-1YP332963K839143M']

    def __init__(self):

        try:
            _ = patreon.config.paypal
        except Exception as exception:
            raise ConfigError(exception)

        try:
            self.__username = patreon.config.paypal['username']
            self.__password = patreon.config.paypal['password']
            self.__api_url = patreon.config.paypal['api_url']
            self.__signature = patreon.config.paypal['signature']
        except Exception as exception:
            raise ConfigError(exception)

    def __make_paypal_request(self, api_method, request_data):
        request_data.update({
            'METHOD': api_method,
            'VERSION': API_VERSION,
            'PWD': self.__password,
            'USER': self.__username,
            'SIGNATURE': self.__signature
        })
        response = requests.post(self.__api_url, data=request_data, timeout=10)
        response_text = response.text

        # TODO log this in redshift

        result_dict = self.__response_to_dictionary(response_text)
        if 'ACK' not in result_dict or not list(result_dict.keys()):
            raise GenericPaypalAPIError(result_dict.get(RESPONSE_BODY_KEY_LONG) or result_dict.get(RESPONSE_BODY_KEY),
                                        request_data.get(TRANSACTION_ID_KEY),
                                        request_data.get(INSTRUMENT_ID_KEY),
                                        request_data.get(AMOUNT_KEY, 0) * 100)

        ack_message = result_dict.get('ACK')
        if not ack_message or (ack_message.lower() != 'success' and ack_message.lower() != 'successwithwarning'):
            raise GenericPaypalAPIError(result_dict.get(RESPONSE_BODY_KEY_LONG) or result_dict.get(RESPONSE_BODY_KEY),
                                        request_data.get(TRANSACTION_ID_KEY),
                                        request_data.get(INSTRUMENT_ID_KEY),
                                        request_data.get(AMOUNT_KEY, 0) * 100)

        return result_dict

    def __response_to_dictionary(self, response):
        result_dict = {}
        for parameter in response.split('&'):
            keyvalue = parameter.split('=', 1)
            if len(keyvalue) == 2:
                result_dict[keyvalue[0]] = unquote(keyvalue[1])

        return result_dict

    @_normalize_exceptions
    def charge_instrument(self, payment_id, instrument_id, amount_cents, description=None):
        amount_dollars = amount_cents / 100
        request_data = {
            AMOUNT_KEY: amount_dollars,
            PAYMENT_ACTION_KEY: 'Sale',
            CURRENCY_KEY: CURRENCY,
            INSTRUMENT_ID_KEY: instrument_id
        }
        if payment_id:
            request_data[IDEMPOTENCE_KEY] = payment_id

        response = self.__make_paypal_request(CHARGE_ACTION, request_data)

        return PaypalChargeResource(response)

    @_normalize_exceptions
    def get_transaction_status(self, transaction_id):
        request_data = {
            TRANSACTION_ID_KEY: transaction_id
        }

        response = self.__make_paypal_request(STATUS_ACTION, request_data)

        return PaypalTransactionResource(response)

    @_normalize_exceptions
    def refund_transaction(self, refund_id, transaction_id):
        request_data = {
            TRANSACTION_ID_KEY: transaction_id,
            CURRENCY_KEY: CURRENCY,
            IDEMPOTENCE_KEY: refund_id
        }
        response = self.__make_paypal_request(REFUND_ACTION, request_data)
        return PaypalRefundResource(response)

    @_normalize_exceptions
    def refund_transaction_partial(self, refund_id, transaction_id, amount_cents):
        amount_dollars = amount_cents / 100
        request_data = {
            TRANSACTION_ID_KEY: transaction_id,
            CURRENCY_KEY: CURRENCY,
            REFUND_TYPE_KEY: 'Partial',
            AMOUNT_KEY: amount_dollars,
            IDEMPOTENCE_KEY: refund_id
        }
        response = self.__make_paypal_request(REFUND_ACTION, request_data)
        return PaypalRefundResource(response)

    @_normalize_exceptions
    def add_instrument(self, instrument_token):
        response = self.__make_paypal_request(CARD_CREATE_ACTION, {'TOKEN': instrument_token})
        return PaypalCardResource(response)

    @_normalize_exceptions
    def add_instrument_start(self, amount_cents, name, description, return_url, cancel_url):

        # These aren't constant-ified because they're all arbitrary and unusued elsewhere
        request_data = {
            'PAYMENTREQUEST_0_AMT': 0,
            'L_PAYMENTREQUEST_0_NAME0': name,
            'L_PAYMENTREQUEST_0_QTY0': 1,
            'L_PAYMENTREQUEST_0_AMT0': 0,
            'RETURNURL': return_url,
            'CANCELURL': cancel_url,
            'PAYMENTREQUEST_0_PAYMENTACTION': 'Sale',
            'PAYMENTREQUEST_0_CURRENCYCODE': CURRENCY,
            'PAYMENTREQUEST_0_CUSTOM': '',
            'NOSHIPPING': 1,
            'TOTALTYPE': 'TOTAL',
            'L_BILLINGTYPE0': 'MerchantInitiatedBillingSingleAgreement',
            'L_BILLINGAGREEMENTDESCRIPTION0': description,

            'MAXAMT': 3 * amount_cents
        }

        response = self.__make_paypal_request('SetExpressCheckout', request_data)

        return response['TOKEN']

    @_normalize_exceptions
    def get_test_instrument_id(self, authorization=None):
        if not patreon.is_test_environment():
            raise TestEnvironmentOnly

        # Thanks paypal for having no interaction-free way to generate billing agreements
        value = self.test_keys[self.test_index]
        self.test_index = (self.test_index + 1) % len(self.test_keys)
        return value

    def raise_generic_api_exception(self, input_exception):
        raise PaypalException(input_exception)
