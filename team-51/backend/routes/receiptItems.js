const { ReceiptItem } = require('../models/receiptItem');
const router = express.Router();

router.get('/', async (req, res) => {
   try {
       const items = await ReceiptItem.find().populate('category');
       res.status(200).json(items);
   } catch (error) {
       res.status(500).json({ error: error.message });
   }
});

router.post('/', async (req, res) => {
   try {
       const item = new ReceiptItem({
           name: req.body.name,
           category: req.body.category,
           cost: req.body.cost,
           quantity: req.body.quantity
       });
       const savedItem = await item.save();
       res.status(201).json(savedItem);
   } catch (error) {
       res.status(500).json({ error: error.message });
   }
});