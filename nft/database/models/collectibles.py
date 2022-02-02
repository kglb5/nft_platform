from app import db


class Collectibles(db.Model):
    id                     =        db.Column(db.Integer, primary_key=True)
    collection_id          =        db.Column(db.String(50), nullable=False)
    collectible_number     =        db.Column(db.Integer, nullable=False, unique=False)
    owner_username         =        db.Column(db.String(30), nullable=False, default='system')


