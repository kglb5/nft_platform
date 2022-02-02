from app import db, redis_client
from nft.database.models.collections import Collections
import uuid


class CollectionsManager:
    @staticmethod
    def create_collection(**kwargs):
        db.session.add(Collections(collection_id=uuid.uuid4().hex,
                                   collection_name=kwargs["collection_name"],
                                   description=kwargs["description"],
                                   creator_username=kwargs["username"],
                                   cover_image_url=kwargs["cover_image_url"],
                                   category=kwargs["category"],
                                   smart_contract_address=kwargs["smart_contract_address"],
                                   fantom_price=kwargs["fantom_price"]
                                   ))
        db.session.commit()
        return {"success": True}

    @staticmethod
    def get_collections(filter, collection_id=None):
        if filter == True:
            query = """SELECT * FROM `black-pearl-nft`.`collections` WHERE (`collection_id` = '{0}')""".format(collection_id)
            result = db.session.execute(query).fetchall()

            collections = {}
            for count, result in enumerate((dict(row) for row in result)):
                collections[count] = {
                    "collection_id": result['collection_id'],
                    "collection_name": result['collection_name'],
                    "description": result['description'],
                    "cover_image_url": result['cover_image_url'],
                    "category": result['category'],
                    "smart_contract_address": result['smart_contract_address'],
                    "fantom_price": result['fantom_price']
                }
            return collections

        if filter == False:
            query = """SELECT * FROM `black-pearl-nft`.`collections`;"""
            result = db.session.execute(query).fetchall()

            collections = {}
            for count, result in enumerate((dict(row) for row in result)):
                collections[count] = {
                    "collection_id": result['collection_id'],
                    "collection_name": result['collection_name'],
                    "description": result['description'],
                    "cover_image_url": result['cover_image_url'],
                    "category": result['category'],
                    "smart_contract_address": result['smart_contract_address'],
                    "fantom_price": result['fantom_price']
                }
            return collections




collection_mgr = CollectionsManager()
