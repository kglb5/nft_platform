from app import db
from datetime import datetime


class Users(db.Model):
    id                           =       db.Column(db.Integer, primary_key=True)
    username                     =       db.Column(db.String(30), unique=True, nullable=False)
    avatar_url                   =       db.Column(db.String(50), unique=False, nullable=True)
    bio                          =       db.Column(db.String(50), unique=False, nullable=True)
    password                     =       db.Column(db.String(150), nullable=False)
    phone_number                 =       db.Column(db.String(50), nullable=True)
    email                        =       db.Column(db.String(100), unique=True, nullable=True)
    role                         =       db.Column(db.String(10), unique=False, nullable=True, default='collector')
    registration_date            =       db.Column(db.DateTime, unique=False, nullable=False, default=datetime.utcnow())


# db.session.add(Users(username='kevinglb14',
#              bio='A good guy',
#              password='non_encrypted',
#              email='kevin@yaxisventures.com'
#              ))
#
# db.session.add(Users(username='ketest',
#              bio='A good guy',
#              password='non_encrypted',
#              email='kevin@teyaxisventures.com'
#              ))
#
# db.session.commit()
