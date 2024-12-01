from pymongo import MongoClient
import datetime

# Connect to MongoDB
client = MongoClient("Your details")
db = client.bestCaption

# Get references to products, offers, purchases, receipts, and users collections
products_collection = db.products
offers_collection = db.offers
purchases_collection = db.purchases
receipts_collection = db.receipts
users_collection = db.users

# Dummy data for Moroccan products with precise categories and marketplace information
products_data = [
    {"_id": 1, "product_name": "Couscous", "category": "Groceries", "price": 20.00, "brand": "Local Brand", "description": "Traditional Moroccan couscous.", "features": ["Organic", "Gluten-Free"], "marketplace": {"name": "Marjane", "location": {"city": "Casablanca", "country": "Morocco"}}, "rating": 4.5},
    {"_id": 2, "product_name": "Couscous", "category": "Groceries", "price": 15.00, "brand": "Premium Couscous Co.", "description": "High-quality couscous with a fine texture.", "features": ["Organic"], "marketplace": {"name": "Carrefour", "location": {"city": "Rabat", "country": "Morocco"}}, "rating": 4.7},
    
    {"_id": 3, "product_name": "Tagine Pot", "category": "Kitchenware", "price": 150.00, "brand": "Ceramic Art", "description": "Authentic Moroccan tagine pot for cooking.", "features": ["Handmade", "Ceramic"], "marketplace": {"name": "Souk", "location": {"city": "Marrakech", "country": "Morocco"}}, "rating": 4.7},
    {"_id": 4, "product_name": "Tagine Pot", "category": "Kitchenware", "price": 120.00, "brand": "Moroccan Kitchen Essentials", "description": "Durable tagine pot for everyday use.", "features": ["Durable", "Ceramic"], "marketplace": {"name": "Aswak Assalam", "location": {"city": "Tangier", "country": "Morocco"}}, "rating": 4.6},
    
    {"_id": 5, "product_name": "Mint Tea", "category": "Beverages", "price": 15.00, "brand": "Moroccan Tea Co.", "description": "Traditional Moroccan mint tea.", "features": ["Refreshing", "Caffeine"], "marketplace": {"name": "Carrefour", "location": {"city": "Rabat", "country": "Morocco"}}, "rating": 4.8},
    {"_id": 6, "product_name": "Mint Tea", "category": "Beverages", "price": 12.00, "brand": "Authentic Mint Tea", "description": "Freshly sourced mint tea leaves.", "features": ["Natural", "Caffeine"], "marketplace": {"name": "Local Market", "location": {"city": "Casablanca", "country": "Morocco"}}, "rating": 4.5},
    
    {"_id": 7, "product_name": "Moroccan Spices Set", "category": "Spices", "price": 50.00, "brand": "Spice World", "description": "A set of essential Moroccan spices.", "features": ["Natural", "Variety"], "marketplace": {"name": "Aswak Assalam", "location": {"city": "Tangier", "country": "Morocco"}}, "rating": 4.6},
    {"_id": 8, "product_name": "Moroccan Spices Set", "category": "Spices", "price": 40.00, "brand": "Moroccan Spice Co.", "description": "Complete spice set for Moroccan cooking.", "features": ["Authentic", "Variety"], "marketplace": {"name": "Marjane", "location": {"city": "Casablanca", "country": "Morocco"}}, "rating": 4.8},
    
    {"_id": 9, "product_name": "Leather Bag", "category": "Fashion", "price": 300.00, "brand": "Artisan Leather", "description": "Handcrafted leather bag.", "features": ["Durable", "Stylish"], "marketplace": {"name": "Marrakech Souk", "location": {"city": "Marrakech", "country": "Morocco"}}, "rating": 4.9},
    {"_id": 10, "product_name": "Leather Bag", "category": "Fashion", "price": 250.00, "brand": "Moroccan Leather Goods", "description": "Elegant leather bag for everyday use.", "features": ["Stylish", "Durable"], "marketplace": {"name": "Souk", "location": {"city": "Fez", "country": "Morocco"}}, "rating": 4.6},
    
    {"_id": 11, "product_name": "Argan Oil", "category": "Beauty", "price": 80.00, "brand": "Argan Essence", "description": "Pure argan oil for skin and hair.", "features": ["Natural", "Moisturizing"], "marketplace": {"name": "Biocoop", "location": {"city": "Agadir", "country": "Morocco"}}, "rating": 4.8},
    {"_id": 12, "product_name": "Argan Oil", "category": "Beauty", "price": 70.00, "brand": "Moroccan Gold", "description": "High-quality argan oil for beauty care.", "features": ["Organic", "Moisturizing"], "marketplace": {"name": "Local Market", "location": {"city": "Casablanca", "country": "Morocco"}}, "rating": 4.7},
    
    {"_id": 13, "product_name": "Moroccan Lantern", "category": "Home Decor", "price": 45.00, "brand": "Artisan Crafts", "description": "Beautifully crafted Moroccan lantern.", "features": ["Handmade", "Decorative"], "marketplace": {"name": "Souk", "location": {"city": "Fez", "country": "Morocco"}}, "rating": 4.4},
    {"_id": 14, "product_name": "Moroccan Lantern", "category": "Home Decor", "price": 35.00, "brand": "Moroccan Home Decor", "description": "Stylish lantern for home decoration.", "features": ["Decorative", "Unique"], "marketplace": {"name": "Aswak Assalam", "location": {"city": "Tangier", "country": "Morocco"}}, "rating": 4.5},
    
    {"_id": 15, "product_name": "Saffron", "category": "Spices", "price": 300.00, "brand": "Premium Saffron", "description": "High-quality Moroccan saffron.", "features": ["Organic", "Aromatic"], "marketplace": {"name": "Aswak Assalam", "location": {"city": "Marrakech", "country": "Morocco"}}, "rating": 4.9},
    {"_id": 16, "product_name": "Saffron", "category": "Spices", "price": 250.00, "brand": "Moroccan Saffron Co.", "description": "Finest saffron for culinary use.", "features": ["Aromatic", "Premium"], "marketplace": {"name": "Marjane", "location": {"city": "Casablanca", "country": "Morocco"}}, "rating": 4.8},
    
    {"_id": 17, "product_name": "Moroccan Bread", "category": "Bakery", "price": 5.00, "brand": "Local Bakery", "description": "Traditional Moroccan bread.", "features": ["Fresh", "Homemade"], "marketplace": {"name": "Local Market", "location": {"city": "Casablanca", "country": "Morocco"}}, "rating": 4.3},
    {"_id": 18, "product_name": "Moroccan Bread", "category": "Bakery", "price": 4.00, "brand": "Artisan Bakery", "description": "Freshly baked Moroccan bread.", "features": ["Soft", "Homemade"], "marketplace": {"name": "Marrakech Souk", "location": {"city": "Marrakech", "country": "Morocco"}}, "rating": 4.4},
    
    {"_id": 19, "product_name": "Kefta Spices", "category": "Spices", "price": 25.00, "brand": "Spice World", "description": "Spices for making Moroccan kefta.", "features": ["Flavorful", "Authentic"], "marketplace": {"name": "Marjane", "location": {"city": "Casablanca", "country": "Morocco"}}, "rating": 4.6},
    {"_id": 20, "product_name": "Kefta Spices", "category": "Spices", "price": 20.00, "brand": "Moroccan Spice Co.", "description": "Perfect blend for Moroccan kefta.", "features": ["Authentic", "Flavorful"], "marketplace": {"name": "Aswak Assalam", "location": {"city": "Tangier", "country": "Morocco"}}, "rating": 4.5}
]

# Dummy data for offers with precise categories and marketplace location data
offers_data = [
    {"_id": 1, "product_name": "Couscous", "discount_percentage": 10, "valid_until": datetime(2024, 12, 31), "category": "Groceries", "offer_details": "Get 10% off on Couscous.", "marketplace": {"name": "Marjane", "location": {"city": "Casablanca", "country": "Morocco"}}},
    {"_id": 2, "product_name": "Tagine Pot", "discount_percentage": 15, "valid_until": datetime(2024, 12, 31), "category": "Kitchenware", "offer_details": "Save 15% on Tagine Pot.", "marketplace": {"name": "Souk", "location": {"city": "Marrakech", "country": "Morocco"}}},
    {"_id": 3, "product_name": "Mint Tea", "discount_percentage": 20, "valid_until": datetime(2024, 12, 31), "category": "Beverages", "offer_details": "20% off on Mint Tea.", "marketplace": {"name": "Carrefour", "location": {"city": "Rabat", "country": "Morocco"}}},
    {"_id": 4, "product_name": "Moroccan Spices Set", "discount_percentage": 5, "valid_until": datetime(2024, 11, 30), "category": "Spices", "offer_details": "Get 5% off on Moroccan Spices Set.", "marketplace": {"name": "Aswak Assalam", "location": {"city": "Tangier", "country": "Morocco"}}},
    {"_id": 5, "product_name": "Leather Bag", "discount_percentage": 12, "valid_until": datetime(2024, 12, 31), "category": "Fashion", "offer_details": "12% discount on Leather Bag.", "marketplace": {"name": "Marrakech Souk", "location": {"city": "Marrakech", "country": "Morocco"}}},
    {"_id": 6, "product_name": "Argan Oil", "discount_percentage": 18, "valid_until": datetime(2024, 12, 31), "category": "Beauty", "offer_details": "Save 18% on Argan Oil.", "marketplace": {"name": "Biocoop", "location": {"city": "Agadir", "country": "Morocco"}}},
    {"_id": 7, "product_name": "Moroccan Lantern", "discount_percentage": 8, "valid_until": datetime(2024, 11, 30), "category": "Home Decor", "offer_details": "8% off on Moroccan Lantern.", "marketplace": {"name": "Souk", "location": {"city": "Fez", "country": "Morocco"}}},
    {"_id": 8, "product_name": "Saffron", "discount_percentage": 10, "valid_until": datetime(2024, 12, 31), "category": "Spices", "offer_details": "Get 10% off on Saffron.", "marketplace": {"name": "Aswak Assalam", "location": {"city": "Marrakech", "country": "Morocco"}}},
    {"_id": 9, "product_name": "Moroccan Bread", "discount_percentage": 5, "valid_until": datetime(2024, 12, 31), "category": "Bakery", "offer_details": "Save 5% on Moroccan Bread.", "marketplace": {"name": "Local Market", "location": {"city": "Casablanca", "country": "Morocco"}}},
    {"_id": 10, "product_name": "Kefta Spices", "discount_percentage": 7, "valid_until": datetime(2024, 12, 31), "category": "Spices", "offer_details": "Save 7% on Kefta Spices.", "marketplace": {"name": "Marjane", "location": {"city": "Casablanca", "country": "Morocco"}}}
]

# Dummy data for users
users_data = [
    {"_id": "12345", "name": "Ahmed", "email": "ahmed@example.com", "location": "Casablanca"},
    {"_id": "67890", "name": "Fatima", "email": "fatima@example.com", "location": "Marrakech"},
    {"_id": "54321", "name": "Youssef", "email": "youssef@example.com", "location": "Rabat"},
    {"_id": "98765", "name": "Amina", "email": "amina@example.com", "location": "Tangier"},
    {"_id": "13579", "name": "Omar", "email": "omar@example.com", "location": "Agadir"}
]

# Dummy data for diverse purchases extracted from user's receipts
purchases_data = [
    # Ahmed's purchases
    {"user_id": "12345", "product_name": "Couscous", "quantity": 2, "purchase_date": "2024-11-29T12:30:00Z", "total_amount": 40.00},
    {"user_id": "12345", "product_name": "Mint Tea", "quantity": 1, "purchase_date": "2024-11-29T12:30:00Z", "total_amount": 15.00},
    {"user_id": "12345", "product_name": "Moroccan Spices Set", "quantity": 1, "purchase_date": "2024-11-29T12:30:00Z", "total_amount": 50.00},
    {"user_id": "12345", "product_name": "Argan Oil", "quantity": 1, "purchase_date": "2024-11-29T12:30:00Z", "total_amount": 80.00},
    
    # Fatima's purchases
    {"user_id": "67890", "product_name": "Tagine Pot", "quantity": 1, "purchase_date": "2024-11-30T14:00:00Z", "total_amount": 150.00},
    {"user_id": "67890", "product_name": "Leather Bag", "quantity": 1, "purchase_date": "2024-11-30T14:00:00Z", "total_amount": 300.00},
    {"user_id": "67890", "product_name": "Mint Tea", "quantity": 2, "purchase_date": "2024-11-30T14:00:00Z", "total_amount": 30.00},
    
    # Youssef's purchases
    {"user_id": "54321", "product_name": "Mint Tea", "quantity": 3, "purchase_date": "2024-11-28T10:00:00Z", "total_amount": 45.00},
    {"user_id": "54321", "product_name": "Argan Oil", "quantity": 2, "purchase_date": "2024-11-28T10:00:00Z", "total_amount": 160.00},
    {"user_id": "54321", "product_name": "Moroccan Spices Set", "quantity": 1, "purchase_date": "2024-11-28T10:00:00Z", "total_amount": 50.00},
    
    # Amina's purchases
    {"user_id": "98765", "product_name": "Moroccan Spices Set", "quantity": 1, "purchase_date": "2024-11-27T16:00:00Z", "total_amount": 50.00},
    {"user_id": "98765", "product_name": "Moroccan Lantern", "quantity": 2, "purchase_date": "2024-11-27T16:00:00Z", "total_amount": 90.00},
    {"user_id": "98765", "product_name": "Kefta Spices", "quantity": 1, "purchase_date": "2024-11-27T16:00:00Z", "total_amount": 25.00},
    
    # Omar's purchases
    {"user_id": "13579", "product_name": "Leather Bag", "quantity": 1, "purchase_date": "2024-11-26T09:00:00Z", "total_amount": 300.00},
    {"user_id": "13579", "product_name": "Saffron", "quantity": 1, "purchase_date": "2024-11-26T09:00:00Z", "total_amount": 300.00},
    {"user_id": "13579", "product_name": "Kefta Spices", "quantity": 3, "purchase_date": "2024-11-26T09:00:00Z", "total_amount": 75.00},
    
    # Additional purchases for diversity
    {"user_id": "12345", "product_name": "Mint Tea", "quantity": 1, "purchase_date": "2024-11-29T12:30:00Z", "total_amount": 15.00},
    {"user_id": "67890", "product_name": "Argan Oil", "quantity": 1, "purchase_date": "2024-11-30T14:00:00Z", "total_amount": 70.00},
    {"user_id": "54321", "product_name": "Moroccan Lantern", "quantity": 1, "purchase_date": "2024-11-28T10:00:00Z", "total_amount": 45.00},
    {"user_id": "98765", "product_name": "Saffron", "quantity": 1, "purchase_date": "2024-11-27T16:00:00Z", "total_amount": 300.00},
    {"user_id": "13579", "product_name": "Couscous", "quantity": 2, "purchase_date": "2024-11-26T09:00:00Z", "total_amount": 40.00}
]

# Dummy data for receipts
receipts_data = [
    {
        "user_location": "Casablanca",
        "user_id": "12345",
        "receipt_id": "67890",
        "purchase_date": "2024-11-29T12:30:00Z",
        "items": [
            {"product_name": "Couscous", "quantity": 2, "brand": "Local Brand", "price": 20, "category": "Groceries"},
            {"product_name": "Mint Tea", "quantity": 1, "brand": "Moroccan Tea Co.", "price": 15, "category": "Beverages"},
            {"product_name": "Moroccan Spices Set", "quantity": 1, "brand": "Spice World", "price": 50, "category": "Spices"},
            {"product_name": "Argan Oil", "quantity": 1, "brand": "Argan Essence", "price": 80, "category": "Beauty"}
        ],
        "total_amount": 85,
        "currency": "MAD"
    },
    {
        "user_location": "Marrakech",
        "user_id": "67890",
        "receipt_id": "67891",
        "purchase_date": "2024-11-30T14:00:00Z",
        "items": [
            {"product_name": "Tagine Pot", "quantity": 1, "brand": "Ceramic Art", "price": 150, "category": "Kitchenware"},
            {"product_name": "Leather Bag", "quantity": 1, "brand": "Artisan Leather", "price": 300, "category": "Fashion"},
            {"product_name": "Mint Tea", "quantity": 2, "brand": "Moroccan Tea Co.", "price": 15, "category": "Beverages"}
        ],
        "total_amount": 465,
        "currency": "MAD"
    },
    {
        "user_location": "Rabat",
        "user_id": "54321",
        "receipt_id": "67892",
        "purchase_date": "2024-11-28T10:00:00Z",
        "items": [
            {"product_name": "Mint Tea", "quantity": 3, "brand": "Moroccan Tea Co.", "price": 15, "category": "Beverages"},
            {"product_name": "Argan Oil", "quantity": 2, "brand": "Argan Essence", "price": 80, "category": "Beauty"},
            {"product_name": "Moroccan Spices Set", "quantity": 1, "brand": "Spice World", "price": 50, "category": "Spices"}
        ],
        "total_amount": 110,
        "currency": "MAD"
    },
    {
        "user_location": "Tangier",
        "user_id": "98765",
        "receipt_id": "67893",
        "purchase_date": "2024-11-27T16:00:00Z",
        "items": [
            {"product_name": "Moroccan Spices Set", "quantity": 1, "brand": "Spice World", "price": 50, "category": "Spices"},
            {"product_name": "Moroccan Lantern", "quantity": 2, "brand": "Artisan Crafts", "price": 45, "category": "Home Decor"},
            {"product_name": "Kefta Spices", "quantity": 1, "brand": "Spice World", "price": 25, "category": "Spices"}
        ],
        "total_amount": 140,
        "currency": "MAD"
    },
    {
        "user_location": "Agadir",
        "user_id": "13579",
        "receipt_id": "67894",
        "purchase_date": "2024-11-26T09:00:00Z",
        "items": [
            {"product_name": "Leather Bag", "quantity": 1, "brand": "Artisan Leather", "price": 300, "category": "Fashion"},
            {"product_name": "Saffron", "quantity": 1, "brand": "Premium Saffron", "price": 300, "category": "Spices"},
            {"product_name": "Kefta Spices", "quantity": 3, "brand": "Spice World", "price": 25, "category": "Spices"},
            {"product_name": "Mint Tea", "quantity": 1, "brand": "Moroccan Tea Co.", "price": 15, "category": "Beverages"}
        ],
        "total_amount": 625,
        "currency": "MAD"
    }
]

# Insert the dummy data into the collections
products_collection.insert_many(products_data)
offers_collection.insert_many(offers_data)
users_collection.insert_many(users_data)
purchases_collection.insert_many(purchases_data)
receipts_collection.insert_many(receipts_data)

print("Products, offers, users, purchases, and receipts have been successfully inserted.")