import asyncio
from datetime import datetime
import logging
from .database import transactions_collection

logger = logging.getLogger(__name__)

class TransactionService:
    async def create_or_find_transaction(self, transaction_data):
        existing_transaction = await transactions_collection.find_one({
            "transaction_id": transaction_data["transaction_id"]
        })
        
        if existing_transaction:
            logger.info(f"Transaction exists: {transaction_data['transaction_id']}")
            return existing_transaction
        
        transaction_data.update({
            "status": "PROCESSING",
            "created_at": datetime.utcnow(),
            "processed_at": None,
            "attempts": 0
        })
        
        result = await transactions_collection.insert_one(transaction_data)
        transaction_data["_id"] = result.inserted_id
        return transaction_data

    async def process_transaction(self, transaction_id):
        try:
            existing_transaction = await transactions_collection.find_one({
                "transaction_id": transaction_id
            })
            
            if not existing_transaction:
                return None
            
            if existing_transaction.get("status") == "PROCESSED":
                return existing_transaction

            logger.info(f"Processing transaction {transaction_id} for 30 seconds...")
            await asyncio.sleep(30)

            await transactions_collection.update_one(
                {"transaction_id": transaction_id},
                {
                    "$set": {
                        "status": "PROCESSED",
                        "processed_at": datetime.utcnow()
                    },
                    "$inc": {"attempts": 1}
                }
            )
            
            logger.info(f"Transaction processed: {transaction_id}")
            
            return await transactions_collection.find_one({"transaction_id": transaction_id})
            
        except Exception as e:
            await transactions_collection.update_one(
                {"transaction_id": transaction_id},
                {
                    "$set": {
                        "status": "FAILED",
                        "processed_at": datetime.utcnow()
                    },
                    "$inc": {"attempts": 1}
                }
            )
            raise e

    async def get_transaction(self, transaction_id):
        return await transactions_collection.find_one({"transaction_id": transaction_id})

    async def get_all_transactions(self):
        cursor = transactions_collection.find().sort("created_at", -1)
        return await cursor.to_list(length=1000)

transaction_service = TransactionService()