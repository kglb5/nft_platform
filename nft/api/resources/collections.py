import requests
from flask import session, make_response, render_template
from app import request, redis_client, Resource, api, reqparse, db
from nft.database.dbm.collections_mgr import collection_mgr
from nft.database.dbm.user_dbm import Users
from nft.helpers.user_accounts import login_required, get_user_id_type

class CreateCollection(Resource):
    method_decorators = [login_required]

    def post(self):

        user = eval("""Users.query.filter_by({0}="{1}").first()""".format(get_user_id_type(session["user_id"]), session["user_id"]))

        data = request.get_json()

        collection_name        =  data["collection_name"]
        description            =  data["description"]

        cover_image_url        =  data["cover_image_url"]
        category               =  data["category"]
        fantom_price           =  data["fantom_price"]
        smart_contract_address =  data["smart_contract_address"]
        creator_username       =  user.username



        return collection_mgr.create_collection(collection_name=collection_name,
                                                description=description,
                                                username=creator_username,
                                                cover_image_url=cover_image_url,
                                                category=category,
                                                smart_contract_address=smart_contract_address,
                                                fantom_price=fantom_price
                                                )
    def put(self):
        pass


class GetCollections(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('collection', type=str)
        arg = parser.parse_args()
        if arg["collection"] == "all":
            return collection_mgr.get_collections(filter=False)
        else:
            return collection_mgr.get_collections(filter=True, collection_id=arg["collection"])

        # if arg == "all":
        #     return collection_mgr.get_collections(filter=False)

class GiftCard(Resource):
    method_decorators = [login_required]
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('gift_card.html'), 200, headers)

class Checkout(Resource):
    method_decorators = [login_required]
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=str)
        arg     = parser.parse_args()
        headers = {'Content-Type': 'text/html'}
        if arg["id"] is None:
            return
        if arg["id"] != "gift_card":
            collection = collection_mgr.get_collections(filter=True, collection_id=arg["id"])[0]

            return make_response(render_template('buy.html', collection=collection), 200, headers)
        return make_response(render_template('gift_card_checkout.html'), 200, headers)


class GetUserCollectibles(Resource):
    method_decorators = [login_required]
    def get(self):
        user   = eval("""Users.query.filter_by({0}="{1}").first()""".format(get_user_id_type(session["user_id"]), session["user_id"]))
        query  = """SELECT * FROM `NFT`.`transactions` WHERE (`transaction_status` = 'confirmed') AND (`username` = '{0}')""".format(user.username)
        result = db.session.execute(query)
        collections = {}
        for count, result in enumerate((dict(row) for row in result)):
            collections[count] = {
                "asset": result['transaction_asset']
            }
        return collections

class Account(Resource):
    method_decorators = [login_required]
    def get(self):
        headers = {'Content-Type': 'text/html'}
        user = eval("""Users.query.filter_by({0}="{1}").first()""".format(get_user_id_type(session["user_id"]), session["user_id"]))
        return make_response(render_template('account.html', user=user), 200, headers)

    def post(self):
        pass

class Test(Resource):
    def get(self):
        url = "https://api.circle.com/v1/configuration"

        payload = {}
        headers = {
            'Accept': 'application/json',
            'Authorization': 'Bearer QVBJX0tFWTo3ZmJkM2MxYjA3OTAzNjljODAxNWI2MzgyZjgwNmIzYTo4ZmZhNmEyMDZlZDYzMmE1YWE1MTYzNGNlMDY4YTFhYQ=='
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        return response.text

api.add_resource(Account, '/account')
api.add_resource(GiftCard, '/gift')
api.add_resource(CreateCollection, '/collection')
api.add_resource(GetUserCollectibles, '/my/collectibles')
api.add_resource(GetCollections, '/collections')
api.add_resource(Checkout, '/checkout')
api.add_resource(Test, '/test')
# api.add_resource(GetCollections, '/<user-id>/collections')
