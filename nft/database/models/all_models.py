from app import db
from nft.database.models.all_models import *
from nft.database.models.payments import *
from nft.database.models.users import *
from nft.database.models.activity import *
from nft.database.models.password_resets import *
from nft.database.models.verification_codes import *
from nft.database.models.collections import *
from nft.database.models.construct import *
from nft.database.models.transaction_history import *
from nft.database.models.social_media_links import *
from nft.database.models.collectibles import *
db.create_all()
