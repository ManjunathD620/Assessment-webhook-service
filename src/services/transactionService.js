const Transaction = require('../models/Transaction');

class TransactionService {
  
  async createOrFindTransaction(transactionData) {
    try {
      
      let transaction = await Transaction.findOne({
        transaction_id: transactionData.transaction_id
      });

      if (transaction) {
        console.log(`Transaction ${transactionData.transaction_id} already exists`);
        return transaction;
      }

      
      transaction = new Transaction(transactionData);
      await transaction.save();
      
      console.log(`Created new transaction: ${transactionData.transaction_id}`);
      return transaction;
    } catch (error) {
      if (error.code === 11000) { 
        
        console.log(`Race condition handled for: ${transactionData.transaction_id}`);
        return await Transaction.findOne({ transaction_id: transactionData.transaction_id });
      }
      throw error;
    }
  }

  
  async processTransaction(transactionId) {
    try {
      console.log(`Starting processing for transaction: ${transactionId}`);
      
      
      const existingTransaction = await Transaction.findOne({ 
        transaction_id: transactionId 
      });
      
      if (!existingTransaction) {
        console.log(`Transaction ${transactionId} not found for processing`);
        return null;
      }

      
      if (existingTransaction.status === 'PROCESSED') {
        console.log(`Transaction ${transactionId} already processed`);
        return existingTransaction;
      }
      
      console.log(`Processing transaction ${transactionId} for 30 seconds...`);
      await new Promise(resolve => setTimeout(resolve, 30000));
      
      
      const transaction = await Transaction.findOneAndUpdate(
        { transaction_id: transactionId },
        {
          status: 'PROCESSED',
          processed_at: new Date(),
          $inc: { attempts: 1 }
        },
        { new: true }
      );

      if (!transaction) {
        console.log(`Transaction ${transactionId} disappeared during processing`);
        return null;
      }

      console.log(`Successfully processed transaction: ${transactionId}`);
      return transaction;
    } catch (error) {
      console.error(`Error processing transaction ${transactionId}:`, error.message);
      
      
      try {
        await Transaction.findOneAndUpdate(
          { transaction_id: transactionId },
          {
            status: 'FAILED',
            processed_at: new Date(),
            $inc: { attempts: 1 }
          }
        );
      } catch (updateError) {
        console.error(`Could not update failed status for ${transactionId}:`, updateError.message);
      }
      
      return null;
    }
  }

  
  async getTransaction(transactionId) {
    return await Transaction.findOne({ transaction_id: transactionId });
  }

  
  async getAllTransactions() {
    return await Transaction.find().sort({ created_at: -1 });
  }
}

module.exports = new TransactionService();