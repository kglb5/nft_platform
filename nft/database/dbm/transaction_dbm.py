from app import db
import uuid
import datetime

from nft.database.models.transaction_history import Transactions

class TransactionManager:
    @staticmethod
    def create_transaction(username, transaction_type, transaction_status, transaction_asset, external_transaction_id=None):
        db.session.add(Transactions(
            transaction_id=str(uuid.uuid4()),
            external_transaction_id=external_transaction_id,
            username=username,
            transaction_time=datetime.datetime.utcnow(),
            transaction_type=transaction_type,
            transaction_status=transaction_status,
            transaction_asset=transaction_asset
        ))
        db.session.commit()


    @staticmethod
    def get_transaction(transaction_id):
        query  = """SELECT * FROM `black-pearl-nft`.`transactions` WHERE `external_transaction_id` = '{}'""".format(transaction_id)
        data   = db.session.execute(query).fetchall()

    @staticmethod
    def update_transaction(transaction_id, status):
        query = """ UPDATE `black-pearl-nft`.`transactions` SET `transaction_status` = '{0}' WHERE `external_transaction_id` = '{1}' """.format(status, transaction_id)
        print(query)
        db.session.execute(query)
        db.session.commit()

transactionManager = TransactionManager()
