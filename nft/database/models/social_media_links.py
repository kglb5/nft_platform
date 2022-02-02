from app import db
from datetime import datetime
import uuid
#
# class SocialMediaLinks(db.Model):
#     id              =       db.Column(db.Integer, primary_key=True)
#     social_media_id =       db.Column(db.String(50), unique=True, nullable=False, default=uuid.uuid4().hex)
#     artist_id       =       db.Column(db.String(40), db.ForeignKey('artists_profiles.artist_id'), unique=False, nullable=False)
#     url             =       db.Column(db.String(150), unique=False, nullable=False)
#     date_added      =       db.Column(db.DateTime, unique=False, nullable=False, default=datetime.utcnow())
