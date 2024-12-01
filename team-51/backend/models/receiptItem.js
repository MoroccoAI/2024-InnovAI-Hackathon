const mongoose = require('mongoose');

const receiptItemSchema = mongoose.Schema({
   name: {
       type: String,
       required: true
   },
   category: {
       type: mongoose.Schema.Types.ObjectId,
       ref: 'Category',
       required: true
   },
   cost: {
       type: Number,
       required: true
   },
   quantity: {
       type: Number,
       required: true
   }
});

exports.ReceiptItem = mongoose.model('ReceiptItem', receiptItemSchema);
