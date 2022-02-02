user_validation_regex = {
        "email":    "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",
        "username": "^(?=.{4,15}$)(?![_.-])(?!.*[_.]{2})[a-zA-Z0-9._-]+(?<![_.])$",
        "password": "^(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*[^\w\d\s:])([^\s]){8,16}$"
    }

support_email_address = "support@blackpearl.nft"

consecutive_login_attempts_in_short_span = "This is your third login attempt, please request a new password or contact support for assitance at {0}.".format(support_email_address)
account_blocked_by_failed_logins_message = "Your account has been blocked after multiple consecutive login attempts. Please contact support at {0} for assistance.".format(support_email_address)

message_templates = {
    1: account_blocked_by_failed_logins_message,
    2: consecutive_login_attempts_in_short_span
}
