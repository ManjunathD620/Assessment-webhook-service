# Transaction Webhook Service

A high-performance backend service for processing payment webhooks with immediate acknowledgment and reliable background processing.

## 🚀 Live Demo

**Base URL:** [https://assessment-webhook-service.onrender.com](https://assessment-webhook-service.onrender.com)

## 📚 API Documentation

### Base URL

[https://assessment-webhook-service.onrender.com](https://assessment-webhook-service.onrender.com)

### Endpoints

#### Health Check

```http
GET /
```

**Response:**

```json
{
    "status": "HEALTHY",
    "current_time": "2024-01-15T10:30:00Z"
}
```

#### Receive Transaction Webhook

```http
POST /v1/webhooks/transactions
```

**Request Body:**

```json
{
    "transaction_id": "txn_abcl23def456",
    "source_account": "acc_user_789",
    "destination_account": "acc_merchant_456",
    "amount": 1500,
    "currency": "INR"
}
```

**Response:**

```json
{
    "status": "accepted",
    "message": "Transaction received and processing started"
}
```

**Status:** `202 Accepted` (within 500ms)

#### Get Single Transaction Status

```http
GET /v1/transactions/{transaction_id}
```

**Response:**

```json
{
    "transaction_id": "txn_abcl23def456",
    "source_account": "acc_user_789",
    "destination_account": "acc_merchant_456",
    "amount": 1500,
    "currency": "INR",
    "status": "PROCESSED",
    "created_at": "2024-01-15T10:30:00Z",
    "processed_at": "2024-01-15T10:30:30Z"
}
```

#### Get All Transactions

```http
GET /v1/transactions
```

**Response:**

```json
[
    {
        "transaction_id": "txn_abcl23def456",
        "source_account": "acc_user_789",
        "destination_account": "acc_merchant_456",
        "amount": 1500,
        "currency": "INR",
        "status": "PROCESSED",
        "created_at": "2024-01-15T10:30:00Z",
        "processed_at": "2024-01-15T10:30:30Z"
    }
]
```

## 🛠️ Tech Stack

- **Backend:** Node.js, Express.js
- **Database:** PostgreSQL with Supabase
- **Deployment:** Render.com
- **Background Processing:** Async/await with setTimeout

## Quick Start

### Prerequisites

- Node.js 16+
- PostgreSQL database (Supabase recommended)

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/ManjunathD620/Assessment-webhook-service.git
cd Assessment-webhook-service
```

2. **Install dependencies**

```bash
npm install
```

3. **Set up environment variables**

```bash
cp .env.example .env
```

Edit `.env` file:

```env
PORT=3000
MONGODB_URI=mongoUrl
NODE_ENV=development
```

4. **Run the application**

```bash
npm start
```

For development with auto-reload:

```bash
npm run dev
```

5. **Access the API**

- API: http://localhost:3000
- Health Check: http://localhost:3000/

## 🧪 Testing the API

### Test Webhook Reception

```bash
curl -X POST "https://assessment-webhook-service.onrender.com/v1/webhooks/transactions" \
  -H "Content-Type: application/json" \
  -d '{
    "transaction_id": "test_txn_001",
    "source_account": "acc_user_123",
    "destination_account": "acc_merchant_456",
    "amount": 1999,
    "currency": "INR"
  }'
```

### Check Transaction Status

```bash
curl "https://assessment-webhook-service.onrender.com/v1/transactions/test_txn_001"
```

### Get All Transactions

```bash
curl "https://assessment-webhook-service.onrender.com/v1/transactions"
```

### Health Check

```bash
curl "https://assessment-webhook-service.onrender.com/"
```
