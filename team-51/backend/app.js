require('dotenv').config();
const express = require('express');
const app = express();
const mongoose = require('mongoose');
const cors = require('cors');


app.use(cors());
app.options('*', cors())

//middleware
app.use(express.json());

//Routes
const receiptsRoutes = require('./routes/receipts');
const receiptItemsRoutes = require('./routes/receiptItems');
const categoriesRoutes = require('./routes/categories');

const api = process.env.API_URL;

app.use(`${api}/receipts`, receiptsRoutes);
app.use(`${api}/items`, receiptItemsRoutes);
app.use(`${api}/categories`, categoriesRoutes);

//Database
mongoose.connect(process.env.CONNECTION_STRING, {
    dbName: 'demodb'
})
.then(()=>{
    console.log('Database Connected')
})
.catch((err)=> {
    console.log(err);
})

//Server
app.listen(3000, ()=>{

    console.log('server is running http://localhost:3000');
})