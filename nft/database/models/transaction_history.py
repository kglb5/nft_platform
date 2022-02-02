from app import db


class Transactions(db.Model):
    id                          =      db.Column(db.Integer, primary_key=True)
    transaction_id              =      db.Column(db.String(50), unique=True, nullable=False)
    external_transaction_id     =      db.Column(db.String(50), unique=False, nullable=True)
    username                    =      db.Column(db.String(30), nullable=False)
    transaction_time            =      db.Column(db.DateTime, unique=False, nullable=False)
    transaction_type            =      db.Column(db.String(40), unique=False, nullable=False)
    transaction_status          =      db.Column(db.String(50), unique=False, nullable=True)
    transaction_asset           =      db.Column(db.String(50), unique=False, nullable=True)
