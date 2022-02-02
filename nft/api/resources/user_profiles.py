from app import Resource, api
from flask import request, render_template, make_response, session
from nft.helpers.user_accounts import login_required, get_user_id_type
from nft.database.dbm.user_dbm import Users

class UserProfile(Resource):
    # method_decorators = [login_required]
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('profile.html'), 200, headers)

class UserProfileData(Resource):
    def get(self):
        user = eval("""Users.query.filter_by({0}="{1}").first()""".format(get_user_id_type(session["user_id"]), session["user_id"]))

        return {
            "username": user.username,
            "bio": user.bio if not "null" else "",
        }
api.add_resource(UserProfile, '/account')
api.add_resource(UserProfileData, '/api/account')
