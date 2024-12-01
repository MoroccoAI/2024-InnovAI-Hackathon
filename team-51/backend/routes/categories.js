const { Category } = require('../models/category');
const express = require('express');
const router = express.Router();

router.get('/', async (req, res) => {
   try {
       const categories = await Category.find();
       res.status(200).json(categories);
   } catch (error) {
       res.status(500).json({ error: error.message });
   }
});

router.post('/', async (req, res) => {
   try {
       const category = new Category({
           name: req.body.name
       });
       const savedCategory = await category.save();
       res.status(201).json(savedCategory);
   } catch (error) {
       res.status(500).json({ error: error.message });
   }
});