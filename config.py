from app import app, redis_client

app.secret_key = 'BAD_SECRET_KEY'

# Configure Redis for storing the session data on the server-side
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_REDIS'] = 'redis_client'


app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://paj4jzh9y732:pscale_pw_Rd1m_K1HW2hIoOuWlrRxQ-hh4fhSL4vRKWtgBbQFuHQ@c1ye4jjak5ml.us-east-3.psdb.cloud:3306/black-pearl-nft?ssl_ca=%2Fetc%2Fssl%2Fcert.pem"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


