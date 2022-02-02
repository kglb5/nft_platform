from app import db
from datetime import datetime
import uuid

class Collections(db.Model):
    id                      =           db.Column(db.Integer, primary_key=True)
    collection_id           =           db.Column(db.String(50), unique=True, nullable=False)
    collection_name         =           db.Column(db.String(60), nullable=False, unique=False)
    description             =           db.Column(db.String(300), nullable=False, unique=False)
    creator_username        =           db.Column(db.String(40), nullable=False)
    cover_image_url         =           db.Column(db.String(200), nullable=False, unique=False)
    release_time            =           db.Column(db.DateTime, unique=False, nullable=False, default=datetime.utcnow())
    end_time                =           db.Column(db.DateTime, unique=False, nullable=True)
    images_urls             =           db.Column(db.String(80), nullable=True, unique=False)
    category                =           db.Column(db.String(80), nullable=False, unique=False)
    listed                  =           db.Column(db.Boolean, nullable=False, default=False)
    items_qty               =           db.Column(db.Integer, nullable=True, unique=False)
    smart_contract_address  =           db.Column(db.String(80), nullable=True, unique=False)
    fantom_price            =           db.Column(db.String(80), nullable=True, unique=False)

