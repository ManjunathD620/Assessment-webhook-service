# Payment Webhook Service

A Node.js webhook service for processing payment transactions with background processing and idempotency. Built for handling transaction webhooks from payment processors like RazorPay.

## 🚀 Live Demo

**API Endpoint:** `https://your-app.vercel.app`

## 📋 Features

- **Fast Webhook Processing**: Responds within 500ms with immediate acknowledgment
- **Background Processing**: 30-second simulated processing with external API calls
- **Idempotent Operations**: Prevents duplicate transaction processing
- **RESTful API**: Clean and well-structured endpoints
- **MongoDB Storage**: Persistent transaction storage
- **Error Handling**: Graceful error handling and validation

## 🛠️ Technical Choices

### Why Node.js + Express?

- **Performance**: Non-blocking I/O handles concurrent webhooks efficiently
- **Ecosystem**: Rich middleware ecosystem for web applications
- **Simplicity**: Quick development and deployment

### Why MongoDB?

- **Flexible Schema**: Easy to evolve transaction data structure
- **Performance**: Fast reads/writes for transaction status checks
- **Idempotency**: Native unique constraints prevent duplicates

### Architecture Decisions

- **Background Processing**: Webhooks respond immediately, process later
- **Idempotency**: Database-level constraints ensure no duplicates
- **Validation**: Request validation before background processing

## 📚 API Documentation

### Base URL
