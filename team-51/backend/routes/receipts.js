const { Receipt } = require('../models/receipt');
const { ReceiptItem } = require('../models/receiptItem');
const { Category } = require('../models/category');
const router = express.Router();

router.get('/', async (req, res) => {
   try {
       const receipts = await Receipt.find().populate({
           path: 'items',
           populate: { path: 'category' }
       });
       res.status(200).json(receipts);
   } catch (error) {
       res.status(500).json({ error: error.message });
   }
});

router.post('/process', async (req, res) => {
   try {
       const receiptData = req.body;
       
       // Save items and get their IDs
       const savedItems = await Promise.all(receiptData.items.map(async (item) => {
           let category = await Category.findOne({ name: item.category });
           if (!category) {
               category = await new Category({ name: item.category }).save();
           }
           
           const receiptItem = new ReceiptItem({
               name: item.name,
               category: category._id,
               cost: item.cost,
               quantity: item.quantity
           });
           return receiptItem.save();
       }));

       // Create receipt with saved item references
       const receipt = new Receipt({
           receipt_id: receiptData.receipt_id,
           date: receiptData.date,
           time: receiptData.time,
           items: savedItems.map(item => item._id),
           total_cost: receiptData.total_cost,
           currency: receiptData.currency
       });

       const savedReceipt = await receipt.save();
       res.status(201).json(savedReceipt);
   } catch (error) {
       res.status(500).json({ error: error.message });
   }
});

module.exports = router;