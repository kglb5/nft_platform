from app import Resource, api, redis_client
from flask import request

import json
import time
import pprint

from nft.database.dbm.transaction_dbm import transactionManager


class TransactionNotification(Resource):
    def post(self):
        data = request.get_json()



        return '', 200


api.add_resource(TransactionNotification, '/transaction_notification')
