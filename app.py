from flask import Flask
from flask_cors import CORS
from flask_restful import Resource, Api, reqparse
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import sqlalchemy
import redis

from nft.database.models.construct import import_models

sqlUrl = sqlalchemy.engine.url.URL(
    drivername="mysql+pymysql",
    username="049tltwpqqug",
    password="pscale_pw_OtawVKcqlcJHwe4qavBeIbDUTpT-EuQoyHi4ginKGjQ",
    host="c1ye4jjak5ml.us-east-3.psdb.cloud",
    port=3306,
    database="black-pearl-nft",
    query={"ssl_ca": "/etc/ssl/cert.pem"},
)
print(sqlUrl)

redis_client = redis.Redis(host='redis-17982.c285.us-west-2-2.ec2.cloud.redislabs.com',
                           password="11nFTiRpmH4XNY1kDBlZ6eus1ZGneSYr",
                           port=17982,
                           db=0)

# for key in redis_client.keys():
#     print(key)
#     print(redis_client.get(key))

app = Flask(__name__)
api = Api(app)
db  = SQLAlchemy(app)


from config import *

from nft.api.resources.users import *
from nft.api.resources.product import *
from nft.api.resources.collections import *
from nft.api.resources.payments import *
from nft.api.resources.webhook import *





if __name__ == '__main__':
    app.run(debug=False, port=5800)
