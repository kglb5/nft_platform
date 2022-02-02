from flask import make_response, render_template
from app import Resource, api, reqparse
from nft.database.dbm.collections_mgr import collection_mgr
from nft.helpers.user_accounts import login_required


class Product(Resource):
    method_decorators = [login_required]
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=str)
        arg = parser.parse_args()
        if arg["id"] is None:
            return
        collection = collection_mgr.get_collections(filter=True, collection_id=arg["id"])[0]
        headers = {'Content-Type': 'text/html'}
        print(collection)
        return make_response(render_template('product.html', collection=collection), 200, headers)

api.add_resource(Product, '/collectible')
