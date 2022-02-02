import requests as r
import uuid
import json


class Circle:
    def __init__(self, env):
        self.env = {
            "sandbox": "https://api-sandbox.circle.com/v1",
            "production": "https://api.circle.com/v1"
        }[env]
        self.api_key = {
            "production": "QVBJX0tFWTo3ZmJkM2MxYjA3OTAzNjljODAxNWI2MzgyZjgwNmIzYTo4ZmZhNmEyMDZlZDYzMmE1YWE1MTYzNGNlMDY4YTFhYQ==",
            "sandbox": "QVBJX0tFWTowNzkyOGE2ZGY2ZmI4MWE1ZGVkMDM1NjE2MWM5YjEwZTo5NjViM2VlMWE4ZmNhYjkxMjQ3MGIzZjY4Y2Q3ZDk4NQ"
        }[env]
        self.headers = {
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Authorization': 'Bearer {0}'.format(self.api_key),
            'Content-Type': 'application/json',
            'Connection': 'keep-alive',
            'User-agent': 'Black Pearl NFT'
        }
        self.proxy_host = "45.77.86.71"
        self.proxy_port = "8080"
        self.proxy_auth = "raj:rj450S@"
        self.proxies = {
            "http": "http://{}@{}:{}/".format(self.proxy_auth, self.proxy_host, self.proxy_port)
        }

    def get_public_key(self):
        return self.base_request(method="get", resource_path="encryption/public", data={})

    def save_card(self, transactor_data):
        data = {
            "idempotencyKey": str(uuid.uuid4()),
            "expMonth": transactor_data["card_exp_month"],
            "expYear": transactor_data["card_exp_year"],
            "keyId": transactor_data["key_id"],
            "encryptedData": transactor_data["full_encrypted_data"],
            "billingDetails": {
                "name": transactor_data["billing_details"]["full_name"],
                "country": transactor_data["billing_details"]["country_code"],
                "district": transactor_data["billing_details"]["district"],
                "line1": transactor_data["billing_details"]["address_line_1"],
                "line2": transactor_data["billing_details"]["address_line_2"],
                "city": transactor_data["billing_details"]["city"],
                "postalCode": transactor_data["billing_details"]["postal_code"]
            },
            "metadata": {
                "email": transactor_data["metadata"]["email"],
                "sessionId": transactor_data["metadata"]["session_id"],
                "ipAddress": transactor_data["metadata"]["ip_address"]

            }
        }
        user_agent = {'User-agent': 'Black Pearl'}
        response = r.post("{0}/cards".format(self.env), headers=self.headers, data=json.dumps(data))

        print(json.dumps(data))

        return response.json()

    def process_payment(self, transactor_data, source_id, card_verification_type="three_d_secure", currency="USD",
                        instrument_type="card"):
        data = {
            "metadata": {
                "email": transactor_data["metadata"]["email"],
                "sessionId": transactor_data["metadata"]["session_id"],
                "ipAddress": transactor_data["metadata"]["ip_address"]
            },
            "amount": {
                "amount": transactor_data["billing_details"]["amount"],
                "currency": currency
            },
            "autoCapture": True,
            "verificationSuccessUrl": "https://9563-148-101-31-62.ngrok.io/successful_transaction",
            "verificationFailureUrl": "https://9563-148-101-31-62.ngrok.io/failed_transaction",
            "source": {
                "id": source_id,
                "type": instrument_type
            },
            "keyId": transactor_data["key_id"],
            "idempotencyKey": str(uuid.uuid4()),
            "verification": "three_d_secure",
            "encryptedData": transactor_data["encrypted_cvv"]
        }

        if card_verification_type != "three_d_secure" or card_verification_type != "cvv":
            data["verification"] = "none"
            del data["encryptedData"]

        return r.request("POST", "{0}/payments".format(self.env), headers=self.headers, data=json.dumps(data)).json()


    def get_payment(self, payment_id):
        return r.get("{0}/payments/{1}".format(self.env, payment_id), headers=self.headers).json()


circle = Circle(env="sandbox")
