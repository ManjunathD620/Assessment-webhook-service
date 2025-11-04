from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
DATABASE_NAME = "payment_webhooks"

client = AsyncIOMotorClient(MONGODB_URI)
database = client[DATABASE_NAME]
transactions_collection = database["transactions"]