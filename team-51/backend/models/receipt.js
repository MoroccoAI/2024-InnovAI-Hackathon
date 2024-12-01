const mongoose = require('mongoose');

const receiptSchema = mongoose.Schema({
   receipt_id: {
       type: String,
       required: true
   },
   date: {
       type: Date,
       required: true
   },
   time: {
       type: String,
       required: true
   },
   items: [{
       type: mongoose.Schema.Types.ObjectId,
       ref: 'ReceiptItem'
   }],
   total_cost: {
       type: Number,
       required: true
   },
   currency: {
       type: String,
       required: true
   }
});

exports.Receipt = mongoose.model('Receipt', receiptSchema);
