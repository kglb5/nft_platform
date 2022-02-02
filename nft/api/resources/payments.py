from app import Resource, api, redis_client
from flask import request, redirect, session, make_response, render_template

from nft.database.dbm.transaction_dbm import transactionManager
from nft.helpers.user_accounts import login_required
from nft.resources.payment_apis.circle import circle

import time
import requests as r
import json

class ProcessPayment(Resource):
    method_decorators = [login_required]
    def post(self):
        data = request.get_json()


        response = r.post("http://10.0.0.9:80/pay",
                          headers={'Content-Type': 'application/json'},
                          data=json.dumps(data)).json()

        payment_data   = response["circle_response"]
        payment_status = payment_data["status"]



        if payment_status == "pending":
            # transactionManager.create_transaction(username=session["user_id"],
            #                                       transaction_type="purchase",
            #                                       transaction_asset=data["transaction_asset"],
            #                                       transaction_status=payment_status,
            #                                       external_transaction_id=payment_data["id"]
            #                                       )
            return make_response(render_template('status_page.html', data=data, href="/", buttonText="Home page", status=payment_status, message="Your payment is pending. You will receive an email notification once it has been processed"), 200, {'Content-Type': 'text/html'})


        if payment_status == "action_required":
            # transactionManager.create_transaction(username=session["user_id"],
            #                                       transaction_type="purchase",
            #                                       transaction_asset=data["transaction_asset"],
            #                                       transaction_status=payment_status,
            #                                       external_transaction_id=payment_data["id"]
            #                                       )
            return redirect(payment_data["requiredAction"]["redirectUrl"])


        if payment_status == "confirmed":

            # transactionManager.create_transaction(username=session["user_id"],
            #                                       transaction_type="purchase",
            #                                       transaction_asset=data["transaction_asset"],
            #                                       transaction_status=payment_status,
            #                                       external_transaction_id=payment_data["id"]
            #                                       )

            return make_response(render_template('status_page.html', data=data, href="/", buttonText="My Collectibles", status=payment_status, message=""), 200, {'Content-Type': 'text/html'})

        if payment_status == "failed":
            headers = {'Content-Type': 'text/html'}
            transactionManager.create_transaction(username=session["user_id"],
                                                  transaction_type="purchase",
                                                  transaction_asset=data["transaction_asset"],
                                                  transaction_status=payment_status,
                                                  external_transaction_id=payment_data["id"]
                                                  )
            return make_response(render_template('status_page.html', data=data, href="/", buttonText="Home Page",
                                                 status=payment_status, message="Your payment failed"), 200, headers)







api.add_resource(ProcessPayment, '/pay')


