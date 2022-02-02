from app import redis_client, Resource, api, db
from flask import request, render_template, make_response
from nft.helpers.user_accounts import login_required, get_user_id_type, validate_account_registration
from nft.database.dbm.activity_dbm import activity_mgr
from nft.database.dbm.user_dbm import activity_mgr, user, session
from nft.database.dbm.user_dbm import Users

import bcrypt


class Main(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('main.html'), 200, headers)


class CreateUser(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('sign_up.html'), 200, headers)

    def post(self):
        data = request.get_json()
        return user.create_user(username=data['username'],
                                email=data['email'],
                                password=data['password'])


class LoginUser(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('login.html'), 200, headers)

    def post(self):
        data = request.get_json()
        user_id  = data["user_id"]
        password = data["password"]

        """Query user password in SQL DB if user_id not in Redis"""
        if redis_client.get(user_id) is None:
            return user.auth_user(user_id=user_id, password=password, request=request)

        """If user_id key in Redis compare submitted password against cached password hash"""
        if bcrypt.checkpw(password.encode('utf-8'), str(redis_client.get(user_id), "utf-8").encode('utf-8')):

            activity_mgr.add_activity(user_id=user_id,
                                      ip=str(request.remote_addr),
                                      user_agent=str(request.user_agent),
                                      activity='user_logged',
                                      url=str(request.url))

            session["user_id"] = user_id
            return {"success": True}

        else:
            return activity_mgr.manage_login_attempts(user_id=user_id, request=request)


class UpdateUser(Resource):
    method_decorators = [login_required]

    def post(self):
        data = request.get_json()
        validation = validate_account_registration(username=data["username"], email=data["email"])

        """If all 4 fields are valid"""
        if validation[1] == 2:
            user = eval("""Users.query.filter_by({0}="{1}").first()""".format(get_user_id_type(session["user_id"]), session["user_id"]))
            query = """UPDATE `NFT`.`users` SET `email` = '{0}' WHERE `email` = "{1}";""".format(data["email"], user.email)
            db.session.execute(query)
            db.session.commit()
            return {"message": "Profile updated"}
        else:
            return validation[0]


class ResetPassword(Resource):
    def get(self):
        return

    def post(self):
        return


# docs.register(Test)

# api.add_resource(Test, '/')
api.add_resource(Main, '/')
api.add_resource(CreateUser, '/signup')
api.add_resource(LoginUser, '/login')
api.add_resource(ResetPassword, '/reset_password')
api.add_resource(UpdateUser, '/update')

# class ResetUserPassword():
#     def post(self):
#         pass
#
#
# class UpdateUser():
#     def post(self):
#         pass


# api.add_resource(ResetUserPassword, '/reset_password')
# api.add_resource(UpdateUser, '/update')
