from fastapi import FastAPI, HTTPException, BackgroundTasks
from datetime import datetime
import logging
from .models import TransactionCreate, TransactionResponse, WebhookResponse, HealthResponse
from .services import transaction_service

logging.basicConfig(
    level=logging.INFO,  
    format="%(asctime)s [%(levelname)s] : %(message)s",
)

logger = logging.getLogger(__name__)

app = FastAPI(title="Payment Webhook Service", version="1.0.0")

@app.get("/", response_model=HealthResponse)
async def health_check():
    return HealthResponse(
        status="HEALTHY",
        current_time=datetime.utcnow()
    )

@app.post("/v1/webhooks/transactions", response_model=WebhookResponse)
async def webhook_transaction(transaction: TransactionCreate, background_tasks: BackgroundTasks):
    if not all([transaction.transaction_id, transaction.source_account, 
                transaction.destination_account, transaction.amount]):
        raise HTTPException(status_code=400, detail="Missing required fields")

    background_tasks.add_task(process_transaction_background, transaction.dict())
    
    logger.info(f"Webhook accepted: {transaction.transaction_id}")
    
    return WebhookResponse(
        status="accepted",
        message="Transaction received and processing started"
    )

@app.get("/v1/transactions/{transaction_id}", response_model=TransactionResponse)
async def get_transaction(transaction_id: str):
    transaction = await transaction_service.get_transaction(transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    return TransactionResponse(
        transaction_id=transaction["transaction_id"],
        source_account=transaction["source_account"],
        destination_account=transaction["destination_account"],
        amount=transaction["amount"],
        currency=transaction["currency"],
        status=transaction["status"],
        created_at=transaction["created_at"],
        processed_at=transaction.get("processed_at")
    )

@app.get("/v1/transactions")
async def get_all_transactions():
    transactions = await transaction_service.get_all_transactions()
    return [
        {
            "transaction_id": t["transaction_id"],
            "source_account": t["source_account"],
            "destination_account": t["destination_account"],
            "amount": t["amount"],
            "currency": t["currency"],
            "status": t["status"],
            "created_at": t["created_at"],
            "processed_at": t.get("processed_at")
        }
        for t in transactions
    ]

async def process_transaction_background(transaction_data):
    try:
        transaction = await transaction_service.create_or_find_transaction(transaction_data)
        await transaction_service.process_transaction(transaction_data["transaction_id"])
        logger.info(f"Processing completed: {transaction_data['transaction_id']}")
    except Exception as e:
        logger.error(f"Processing failed: {transaction_data['transaction_id']}")