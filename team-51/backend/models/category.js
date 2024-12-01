const mongoose = require('mongoose');

const categorySchema = mongoose.Schema({
   name: {
       type: String,
       required: true,
       unique: true
   }
});

exports.Category = mongoose.model('Category', categorySchema);