from patreon.constants.error_level import ErrorLevel
from patreon.constants.http_codes import INVALID_REQUEST_400
from patreon.exception import ResourceMissing, APIException


class UserNotFound(ResourceMissing):
    def __init__(self, user_id):
        super().__init__('User', user_id)


class PasswordTooShort(APIException):
    status_code = INVALID_REQUEST_400
    error_title = "Your password is too short. It must be at least 6 characters long"
    error_level = ErrorLevel.INFO
