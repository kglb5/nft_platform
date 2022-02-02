from app import db
from datetime import datetime
import uuid

class Activity(db.Model):
    id              =       db.Column(db.Integer, primary_key=True)
    activity_id     =       db.Column(db.String(50), unique=True, nullable=False, default=uuid.uuid4().hex)
    user_id         =       db.Column(db.String(40), unique=False, nullable=True)
    ip              =       db.Column(db.String(20), unique=False, nullable=True)
    user_agent      =       db.Column(db.String(80), unique=False, nullable=True)
    time            =       db.Column(db.DateTime, unique=False, nullable=False, default=datetime.utcnow())
    activity        =       db.Column(db.String(20), unique=False, nullable=False)
    url             =       db.Column(db.String(100), unique=False, nullable=False)
