from patreon.constants.error_level import ErrorLevel
from patreon.constants.http_codes import RESOURCE_CONFLICT_409, NOT_AUTHORIZED_403, AUTHENTICATION_REQUIRED_401, \
    INVALID_REQUEST_400
from patreon.exception import APIException, PatreonException, ParameterInvalid


class InvalidUser(APIException):
    status_code = NOT_AUTHORIZED_403
    error_title = "Incorrect email or password."
    error_level = ErrorLevel.INFO


class BlankPassword(APIException):
    status_code = NOT_AUTHORIZED_403
    error_title = "Your password is invalid. Please use the 'Forgot Password?' link below to reset it."
    error_level = ErrorLevel.INFO


class UserAlreadyExists(APIException):
    status_code = RESOURCE_CONFLICT_409
    error_title = "This email address already has a Patreon account."
    error_level = ErrorLevel.INFO


class CSRFFailed(APIException):
    status_code = NOT_AUTHORIZED_403
    error_title = "CSRF Failure"
    error_level = ErrorLevel.INFO


class CSRFExpired(CSRFFailed):
    error_title = "Your CSRF token has expired"


class UnauthorizedAdminFunction(PatreonException):
    pass


class UnauthorizedAdminAPIRoute(UnauthorizedAdminFunction, APIException):
    status_code = NOT_AUTHORIZED_403
    error_title = "Not authorized to access route"
    error_level = ErrorLevel.INFO


class TwoFactorRequired(APIException):
    status_code = AUTHENTICATION_REQUIRED_401
    error_title = "2fa_required"
    error_description = "Two Factor Auth Required"
    error_level = ErrorLevel.INFO


class TwoFactorInvalid(APIException):
    status_code = NOT_AUTHORIZED_403
    error_title = "2fa_invalid"
    error_description = "Two Factor Auth code invalid"
    error_level = ErrorLevel.INFO


class BadCaptcha(APIException):
    status_code = INVALID_REQUEST_400
    error_title = "Bad captcha response"
    error_level = ErrorLevel.INFO


class ResetPasswordInvalidEmail(ParameterInvalid):
    def __init__(self, parameter_name, parameter_value):
        super().__init__(parameter_name=parameter_name,
                         parameter_value=parameter_value)
        self.error_description = "No user found with that email address."


class ResetPasswordUserHasNoPassword(ParameterInvalid):
    def __init__(self, parameter_name, parameter_value):
        super().__init__(parameter_name=parameter_name,
                         parameter_value=parameter_value)
        self.error_description = "No password was ever set for this email address."
