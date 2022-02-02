from patreon.constants.error_level import ErrorLevel
from patreon.constants.http_codes import INTERNAL_SERVER_ERROR_500, INVALID_REQUEST_400, NOT_FOUND_404
from patreon.exception import PatreonException, APIException


class PaymentException(PatreonException):
    pass


class ExternalPaymentAPIException(PaymentException):
    def __init__(self, exception, transaction_id=None, instrument_id=None, amount_cents=None):
        self.original_exception = exception
        self.transaction_id = transaction_id
        self.instrument_id = instrument_id
        self.amount_cents = amount_cents

    def __str__(self):
        return "{}: {} (TransactionID: {}, InstrumentID: {}, Amount Cents: {})".format(
            self.original_exception.__class__.__name__,
            str(self.original_exception),
            self.transaction_id,
            self.instrument_id,
            self.amount_cents)

    def to_dict(self):
        return {
            'transaction_id': self.transaction_id,
            'instrument_id': self.instrument_id,
            'amount_cents': self.amount_cents
        }


class UnrecoverablePaymentFailure(PaymentException):
    pass


class RecoverablePaymentFailure(PaymentException):
    pass


class TemporaryUnrecoverablePaymentFailure(PaymentException):
    pass


class GenericPaypalAPIError(PaymentException):
    def __init__(self, message, transaction_id=None, instrument_id=None, amount_cents=None):
        self.message = message
        self.transaction_id = transaction_id
        self.instrument_id = instrument_id
        self.amount_cents = amount_cents

    def __str__(self):
        return self.message

    def to_dict(self):
        return {
            'original_exception': self.message,
            'transaction_id': self.transaction_id,
            'instrument_id': self.instrument_id,
            'amount_cents': self.amount_cents
        }


class TemporaryOutage(RecoverablePaymentFailure, ExternalPaymentAPIException):
    pass


class CardDeclineError(UnrecoverablePaymentFailure, ExternalPaymentAPIException):
    pass


class CardDeclineFraudError(CardDeclineError):
    pass


class CardDeclineMonthlyMaxError(CardDeclineError):
    pass


class CardDeclineEmergencyError(CardDeclineError):
    pass


class CancelledBillingAgreement(GenericPaypalAPIError):
    pass


class PendingPaypalTransaction(GenericPaypalAPIError):
    pass


class AuthenticationError(TemporaryUnrecoverablePaymentFailure, ExternalPaymentAPIException):
    pass


class InvalidAPIRequest(TemporaryUnrecoverablePaymentFailure, ExternalPaymentAPIException):
    pass


class ReusedIdempotencyKey(InvalidAPIRequest):
    pass


class ChargeFailed(UnrecoverablePaymentFailure):
    def __init__(self, external_payment_id, exception=None):
        self.original_exception = exception
        self.external_payment_id = external_payment_id

    def __str__(self):
        return "{}: {} (ExternalPaymentID {})".format(
            self.original_exception.__class__.__name__,
            str(self.original_exception),
            self.external_payment_id
        )

    def to_dict(self):
        return {
            'external_payment_id': self.external_payment_id
        }


class LedgerEntrySanityCheckFail(TemporaryUnrecoverablePaymentFailure):
    def __init__(self, transaction_id, running_total):
        self.transaction_id = transaction_id
        self.running_total = running_total

    def __str__(self):
        return "Ledger amounts sum to {} instead of 0 for transaction {}".format(self.running_total,
                                                                                 self.transaction_id)

    def to_dict(self):
        return {
            'transaction_id': self.transaction_id,
            'running_total': self.running_total
        }


class AccountNotFound(PaymentException):
    def __init__(self, type, user_id, payment_instrument_id, campaign_id, system_classificaiton):
        self.type = type
        self.user_id = user_id
        self.payment_instrument_id = payment_instrument_id
        self.campaign_id = campaign_id
        self.system_classification = system_classificaiton

    def __str__(self):
        return "Account not found (type: {}, user id: {}, payment instrument id: {}, campaign_id: {}, system_classification: {})".format(
            self.type,
            self.user_id,
            self.payment_instrument_id,
            self.campaign_id,
            self.system_classification)

    def to_dict(self):
        return {
            'type': self.type,
            'user_id': self.user_id,
            'payment_instrument_id': self.payment_instrument_id,
            'campaign_id': self.campaign_id,
            'system_classification': self.system_classification
        }


class GenericCodeFailure(TemporaryUnrecoverablePaymentFailure, ExternalPaymentAPIException):
    # This is just something to wrap rando exceptions like... encoding exceptions or dict access errors
    # Things that aren't specific to payments code, but are thrown by payments code, and thus, are more severe than normal
    pass


class ConfigError(TemporaryUnrecoverablePaymentFailure, ExternalPaymentAPIException):
    pass


class UnexpectedPaypalAPIError(UnrecoverablePaymentFailure, ExternalPaymentAPIException):
    pass


class PaymentExceptionForAPI(APIException, PaymentException):
    status_code = INVALID_REQUEST_400
    error_level = ErrorLevel.INFO

    def __init__(self, exception=None):
        self.original_exception = exception

    def to_dict(self):
        return {
            'error_level': self.error_level.name,
            'error_title': self.error_title,
            'status_code': self.status_code,
            'error_description': self.error_description
        }


class MissingStripeToken(PaymentExceptionForAPI):
    error_type = "missing_stripe_token"
    error_title = "Stripe token is required."


class BadCardAuthorizationToken(PaymentExceptionForAPI):
    error_type = "bad_stripe_token"
    error_title = "Unable to get customer information from token."


class StripeException(PaymentExceptionForAPI):
    error_type = "stripe_exception"
    error_title = "Error Communicating with Stripe."


class PaypalException(PaymentExceptionForAPI):
    error_type = "paypal_exception"
    error_title = "Error Communicating with PayPal."


class CardNotFound(PaymentExceptionForAPI):
    error_type = 'card_not_found'
    error_title = 'Card does not exist'


class InvalidCardToken(PaymentExceptionForAPI):
    error_type = 'bad_card_token_type'
    error_title = 'Card type Not Recognized'


class InvalidCardAuthorization(PaymentExceptionForAPI):
    error_type = 'bad_card_authorization_type'
    error_title = 'Card authorization token type Not Recognized'


class NotCardOwner(PaymentExceptionForAPI):
    error_type = 'not_card_owner'
    error_title = 'User is not owner of requested card'


class BigMoneyChargeError(PaymentExceptionForAPI):
    error_type = 'generic_big_money_charge_error'
    error_title = 'Big money charge failed'


class PledgeCreationError(PaymentExceptionForAPI):
    status_code = INTERNAL_SERVER_ERROR_500
    error_type = "generic_pledge_error"
    error_title = "We were not able to save your pledge."
    error_level = ErrorLevel.ERROR


class PledgeNotFound(PaymentExceptionForAPI):
    status_code = NOT_FOUND_404
    error_type = "pledge_not_fount"
    error_title = "Pledge not found."
    error_level = ErrorLevel.INFO


class TimeNotEpoch(APIException):
    status_code = INVALID_REQUEST_400
    error_type = "bad_time"

    error_level = ErrorLevel.ERROR

    def __init__(self, time):
        self.error_title = "{} is not a unix epoch".format(time)


class TransactionAlreadyFailed(UnrecoverablePaymentFailure):
    def __init__(self, id, type):
        self.id = id
        self.type = type

    def to_dict(self):
        return {
            'type': self.type,
            'id': self.id
        }

    def __str__(self):
        return "Transaction {} of type {} has failed and cannot be retried".format(self.id, self.type)


class TransactionInProcess(RecoverablePaymentFailure):
    def __init__(self, id, type):
        self.id = id
        self.type = type

    def to_dict(self):
        return {
            'type': self.type,
            'id': self.id
        }

    def __str__(self):
        return "Transaction {} of type {} is already being processed".format(self.id, self.type)


class ExternalPaymentAlreadyFailed(UnrecoverablePaymentFailure):
    def __str__(self):
        return "External Payment has already failed, cannot process"


class TransactionTypeUnhandled(TemporaryUnrecoverablePaymentFailure):
    def __init__(self, type):
        self.type = type

    def to_dict(self):
        return {
            'type': self.type
        }

    def __str__(self):
        return "Transaction type {} has no handler".format(self.type.name)


class TransactionTypeDoesntExist(TemporaryUnrecoverablePaymentFailure):
    def __init__(self, type):
        self.type = type

    def to_dict(self):
        return {
            'type': self.type
        }

    def __str__(self):
        return "Transaction type {} not recognized".format(self.type)


class TransactionNotExist(UnrecoverablePaymentFailure):
    def __init__(self, id):
        self.id = id

    def to_dict(self):
        return {
            'id': self.id
        }

    def __str__(self):
        return "Transaction {} does not exist".format(self.id)
