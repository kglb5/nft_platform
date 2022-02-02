from app import db
from nft.database.models.collectibles import Collectibles


class CollectibleDBM:

    @staticmethod
    def create_collectible(collection_id, collectible_number, owner_username):
        db.session.add(Collectibles(
            collection_id=collection_id,
            collectible_number=collectible_number,
            owner_username=owner_username
        ))
        db.session.commit()



    @staticmethod
    def update_collectible():
        pass


    @staticmethod
    def delete_collectible():
        pass



    @staticmethod
    def get_all_collectibles_by_owner():
        pass


    @staticmethod
    def get_all_collection_collectibles():
        pass
