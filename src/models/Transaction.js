const mongoose = require('mongoose');

const transactionSchema = new mongoose.Schema({
  transaction_id: {
    type: String,
    required: true,
    unique: true,
    index: true
  },
  source_account: {
    type: String,
    required: true
  },
  destination_account: {
    type: String,
    required: true
  },
  amount: {
    type: Number,
    required: true
  },
  currency: {
    type: String,
    required: true,
    default: 'INR'
  },
  status: {
    type: String,
    enum: ['PROCESSING', 'PROCESSED', 'FAILED'],
    default: 'PROCESSING'
  },
  created_at: {
    type: Date,
    default: Date.now
  },
  processed_at: {
    type: Date,
    default: null
  },
  attempts: {
    type: Number,
    default: 0
  }
});


transactionSchema.index({ transaction_id: 1, status: 1 });

module.exports = mongoose.model('Transaction', transactionSchema);