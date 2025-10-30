const express = require('express');
const router = express.Router();
const transactionService = require('../services/transactionService');


router.get('/', (req, res) => {
  res.json({
    status: 'HEALTHY',
    current_time: new Date().toISOString()
  });
});





router.post('/v1/webhooks/transactions', (req, res) => {
    const startTime = Date.now();
    
    try {
        const { transaction_id, source_account, destination_account, amount, currency } = req.body;

        if (!transaction_id || !source_account || !destination_account || !amount) {
            return res.status(400).json({
                error: "Missing required fields"
            });
        }

        res.status(202).json({
            status: "accepted",
            message: "Transaction received and processing started"
        });

        processBackground(transaction_id, {
            transaction_id,
            source_account, 
            destination_account,
            amount,
            currency: currency || 'INR'
        }).catch(error => {
            console.error(`Background processing failed for ${transaction_id}:`, error);
        });

    } catch (error) {
        console.error('Webhook error:', error);
        
        const elapsed = Date.now() - startTime;
        if (elapsed < 500) {
            res.status(202).json({
                status: "accepted", 
                message: "Request received successfully"
            });
        } else {
            res.status(202).end();
        }
    }
});

async function processBackground(transactionId, transactionData) {
    try {
        console.log(`Starting background processing for: ${transactionId}`);
        
        const transaction = await transactionService.createOrFindTransaction(transactionData);
        await transactionService.processTransaction(transactionId);
        
        console.log(`Background processing completed for: ${transactionId}`);
    } catch (error) {
        console.error(`Background processing failed for ${transactionId}:`, error);
    }
}


router.get('/v1/transactions/:transaction_id', async (req, res) => {
  try {
    const { transaction_id } = req.params;
    const transaction = await transactionService.getTransaction(transaction_id);

    if (!transaction) {
      return res.status(404).json({
        error: 'Transaction not found'
      });
    }

    res.json({
      transaction_id: transaction.transaction_id,
      source_account: transaction.source_account,
      destination_account: transaction.destination_account,
      amount: transaction.amount,
      currency: transaction.currency,
      status: transaction.status,
      created_at: transaction.created_at,
      processed_at: transaction.processed_at
    });

  } catch (error) {
    console.error('Get transaction error:', error);
    res.status(500).json({
      error: 'Internal server error'
    });
  }
});


router.get('/v1/transactions', async (req, res) => {
  try {
    const transactions = await transactionService.getAllTransactions();
    res.json(transactions);
  } catch (error) {
    console.error('Get all transactions error:', error);
    res.status(500).json({
      error: 'Internal server error'
    });
  }
});

module.exports = router;