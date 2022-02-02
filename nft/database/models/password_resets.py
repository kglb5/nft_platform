from app import db
from datetime import datetime
import uuid


class PasswordResets(db.Model):
    id                  =       db.Column(db.Integer, primary_key=True)
    username            =       db.Column(db.String(30), nullable=False)
    reset_code          =       db.Column(db.String(50), unique=True, nullable=False, default=uuid.uuid4().hex)
    date_requested      =       db.Column(db.DateTime, nullable=False, unique=False)
    time                =       db.Column(db.DateTime, unique=False, nullable=False, default=datetime.utcnow())
    expiration_time     =       db.Column(db.DateTime, unique=False, nullable=False)
