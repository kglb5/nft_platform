from flask import session

from app import db, redis_client

from nft.database.dbm.activity_dbm import activity_mgr
from nft.database.models.users import Users
from nft.database.models.verification_codes import VerificationCodes
from nft.helpers.user_accounts import get_user_id_type, validate_account_registration


import bcrypt
import uuid




class User:
    @staticmethod
    def create_user(**kwargs):
        validation = validate_account_registration(**kwargs)

        """If all 4 fields are valid"""
        if validation[1] == 3:

            if db.session.query(db.exists().where(Users.username == kwargs['username'])).scalar():
                return {"success": False,
                        "field": "username",
                        "message": "We’re sorry, this username is not available. Please enter another username and try again, or login to your existing account."}

            if db.session.query(db.exists().where(Users.email == kwargs['email'])).scalar():
                return {"success": False,
                        "field": "email",
                        "message": "This email address is already exists. Please try a different email address to sign-up, or login to your existing account."}

            db.session.add(Users(username=kwargs['username'],
                                 email=kwargs['email'],
                                 password=bcrypt.hashpw(kwargs['password'].encode('UTF-8'), bcrypt.gensalt())))

            db.session.add(VerificationCodes(username=kwargs['username'], verification_Code=uuid.uuid4().hex))
            db.session.commit()

            session["user_id"] = kwargs['username']
            return {"success": True}

        else:
            """Returns valid and invalid fields"""
            return {
                     "valid_fields": validation[0],
                     "success": False
                   }


    @staticmethod
    def auth_user(user_id, password, request):

        user_id_type = get_user_id_type(user_id)
        user         = eval("""Users.query.filter_by({0}="{1}").first()""".format(user_id_type, user_id))

        if user is None:
            return {
                    "success": False,
                    "message": "This username don't exist"
                }

        if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):

            redis_client.set(user_id, user.password)

            session["user_id"] = user_id

            activity_mgr.add_activity(user_id=user_id,
                                      ip=str(request.remote_addr),
                                      user_agent=str(request.user_agent),
                                      activity='user_logged',
                                      url=str(request.url))
            return {"success": True}
        else:
            return activity_mgr.manage_login_attempts(user_id=user_id, request=request)




    @staticmethod
    def update_user(detail):
        editable_details = ['email', 'username', 'password', 'bio', 'avatar', '']
        if detail not in editable_details:
            pass



    @staticmethod
    def deactivate_user():
        pass



    @staticmethod
    def get_user_profile():
        pass


user = User()
