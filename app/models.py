from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class TransactionCreate(BaseModel):
    transaction_id: str
    source_account: str
    destination_account: str
    amount: float
    currency: str = "INR"

class TransactionResponse(BaseModel):
    transaction_id: str
    source_account: str
    destination_account: str
    amount: float
    currency: str
    status: str
    created_at: datetime
    processed_at: Optional[datetime] = None

class WebhookResponse(BaseModel):
    status: str
    message: str

class HealthResponse(BaseModel):
    status: str
    current_time: datetime