from app import db
from datetime import datetime
import uuid


class Payments(db.Model):
    id                          =           db.Column(db.Integer, primary_key=True)
    payment_id                  =           db.Column(db.String(50), unique=True, nullable=False, default=uuid.uuid4().hex)
    external_transaction_id     =           db.Column(db.String(50), unique=False, nullable=False)
    payer_username              =           db.Column(db.String(30), nullable=False)
    amount                      =           db.Column(db.Integer, nullable=False, unique=False)
    payment_method              =           db.Column(db.DateTime, unique=False, nullable=False, default=datetime.utcnow())
    card_number                 =           db.Column(db.String(40), unique=False, nullable=False)
    payment_status              =           db.Column(db.String(50), unique=False, nullable=False)
    payment_description         =           db.Column(db.String(30), nullable=False, unique=False)
