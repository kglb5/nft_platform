from flask import session, redirect
import flask_restful
import re
import functools

from app import db
from constants import user_validation_regex
from nft.database.models.users import Users


def get_user_id_type(user_id):
    user_id_type = "username"

    """Update id_type for email if string match email regex"""
    if re.compile("^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$").match(user_id):
        user_id_type = "email"

    return user_id_type


def validate_account_registration(**kwargs):
    valid_fields_count = 0
    valid_fields = {}
    for key, value in kwargs.items():
        if re.compile(user_validation_regex[key]).match(value):
            valid_fields[key] = True
            valid_fields_count += 1
        else:
            valid_fields[key] = False
    return valid_fields, valid_fields_count



def login_required(func):
    @functools.wraps(func)
    def secure_function():
        if "user_id" not in session:
            return redirect("/login", code=302)
        else:
            return func()

    return secure_function
