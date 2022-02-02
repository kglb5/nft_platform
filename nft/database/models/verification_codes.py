from app import db


class VerificationCodes(db.Model):
    id                      =           db.Column(db.Integer, primary_key=True)
    username                =           db.Column(db.String(50), unique=False, nullable=False)
    verification_Code       =           db.Column(db.String(50), unique=True, nullable=False)
    is_verified             =           db.Column(db.Boolean, nullable=False, default=False)
    date_verified           =           db.Column(db.DateTime, nullable=True, default=None)


