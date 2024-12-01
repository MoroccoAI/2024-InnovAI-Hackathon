from flask import Flask, jsonify, request
import xgboost as xgb
import holidays
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import json
import pymongo
from openai import OpenAI
from pydantic import BaseModel
from typing import List
from datetime import datetime, timedelta, timezone
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

app = Flask(__name__)

# MongoDB connection setup
MONGO_DETAILS = os.getenv("MONGO_DETAILS")
client = pymongo.MongoClient(MONGO_DETAILS)
database = client.bestCaption
user_collection = database.get_collection("users")
receipts_collection = database.get_collection("receipts")
purchases_collection = database.get_collection("purchases")
offers_collection = database.get_collection("offers")
products_collection = database.get_collection("products")

# OpenAI API setup
openai_api_key = os.getenv("OPENAI_API_KEY")  # Use environment variable for OpenAI API key
openai_client = OpenAI(api_key=openai_api_key)

# Define the schema for parsing
class ReceiptItem(BaseModel):
    name: str
    cost: float
    quantity: int
    category: str

class Receipt(BaseModel):
    receipt_id: str
    date: str
    time: str
    items: List[ReceiptItem]
    total_cost: float
    currency: str

# Define MongoDB schemas
class MongoReceipt(BaseModel):
    user_location: str
    user_id: str
    receipt_id: str
    purchase_date: datetime
    items: List[ReceiptItem]
    total_amount: float
    currency: str

class MongoPurchase(BaseModel):
    user_id: str
    product_name: str
    quantity: int
    purchase_date: datetime
    total_amount: float

def extract_date(date_string):
  try:
    return pd.to_datetime(date_string).date()
  except ValueError:
    return None


def is_last_two_weeks_of_august(date):
    """
    Check if the given date is part of the last two weeks of August.
    """
    year = date.year
    start_of_last_two_weeks = datetime(year, 8, 18).date()  # Start date: August 18
    end_of_august = datetime(year, 8, 31).date()           # End date: August 31
    return start_of_last_two_weeks <= date <= end_of_august

def is_n_days_after(given_date, event_date, n):
    """
    """
    return event_date - timedelta(days=n) <=given_date <= event_date

def generate_feature_array(date):
    feature_array = [0,0,0] # fitr (ramadan), adha, then school year start (in order)

    ma_holidays = holidays.country_holidays('MA', years=[date.year, date.year+1])

    fitr = ma_holidays.get_named('al-Fitr')
    adha = ma_holidays.get_named('al-Adha')

    for day in fitr:
      if is_n_days_after(date, day, 35):
          feature_array[0] = 1
          break

    for day in adha:
      if is_n_days_after(date, day, 15):
           feature_array[1] = 1
           break


    if is_last_two_weeks_of_august(date):
          feature_array[2] = 1

    return feature_array

def get_recent_purchases(user_id, limit):
    recent_purchases = list(purchases_collection.find(
        {
            "user_id": user_id, 
            "purchase_date": {"$gte": datetime.now(timezone.utc) - timedelta(days=int(limit))}
        }
    ))
    return recent_purchases

def get_similar_products_and_offers(purchased_items):
    similar_products = []
    discounts = []
    
    for item in purchased_items:
        query = {"category": item["category"], "product_name": item["product_name"]}
        products = list(products_collection.find(query))
        
        if products:
            similar_products.append(products)
        
        offers = list(offers_collection.find({"product_name": item["product_name"], "valid_until": {"$gte": datetime.utcnow()}}))
        if offers:
            discounts.extend(offers)
    
    return similar_products, discounts

def one_hot_encode_category(category_string):
  """
  One-hot encodes a category string.

  Args:
    category_string: The category string to encode.

  Returns:
    A NumPy array representing the one-hot encoded category.
  """
    # all_categories: A list of all possible categories.
  all_categories = ['Sports', 'Clothing', 'Toys', 'Beauty', 'Books', 'Home & Kitchen', 'Electronics']
  encoded_category = np.zeros(len(all_categories), dtype=int)
  index = all_categories.index(category_string)
  encoded_category[index] = 1
    
  return encoded_category

@app.route('/predict', methods=['POST'])
def predict():
    # needs a category string + a date of purchase + cost 
    delta = 0.20
    observed_cost = request.json['cost']
    date_of_purchase = extract_date(request.json['date_of_purchase'])
    category_array = one_hot_encode_category(request.json['category'])
    input_array = np.array()
    model = xgb.XGBRegressor()
    model.load_model('xgboost_model.json')
    day_array = generate_feature_array(date_of_purchase)
    input_array = np.concatenate([day_array, category_array])
    input_array = input_array.reshape(1, -1)
    predicted_value = model.predict(input_array)

    if predicted_value > observed_cost * (1+delta):
        return jsonify({"status": "success", "out_of_bounds": True, 'predicted_cost': predicted_value}), 200
    else:
        return jsonify({"status": "success", "out_of_bounds": False, 'predicted_cost': predicted_value}), 200




@app.route('/receipt', methods=['POST'])
def upload_receipt():
    if 'image' not in request.json:
        return jsonify({"status": "error", "message": "No image part"}), 400
    base64_image = request.json['image']
    if not base64_image:
        return jsonify({"status": "error", "message": "No image provided"}), 400

    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": """
The image contains a receipt. Please extract the information in JSON format, including the receipt’s unique id, date (in ‘YYYY-MM-DD’ format), and time (in ‘HH:MM:SS’ format). For each item, list the name (including any volume or mass, such as ‘Milk 1L’ or ‘Tomatoes 500g’), cost (as a decimal number), quantity (as an integer), category (such as ‘sweets’, ‘dairy’, ‘vegetables’, ‘fruit’, ‘pasta’, etc.), and the currency used. Include the total cost of the receipt (a decimal number) and the currency used for the total. Ensure the JSON is properly structured and formatted.
                    """,
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    },
                },
            ],
        }
    ]

    try:
        response = openai_client.beta.chat.completions.parse(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0,
            response_format=Receipt
        )
        structured_data = json.loads(response.choices[0].message.content)
        #TESTING WITH 12345 USER
        user_id = request.form.get('user_id', "12345")
        
        total_cost = structured_data['total_cost']
        receipt_id = f"{total_cost}_{structured_data.get('date', '1970-01-01').replace('-', '')}_{structured_data.get('time', '00:00:00').replace(':', '')}"
        existing_receipt = receipts_collection.find_one({"receipt_id": receipt_id})
        if existing_receipt:
            return jsonify({"status": "error", "message": "Receipt already scanned."}), 400
        
        ##############################################################
        # Note: Saving receipt and user purchases should be done by the second backend,
        #  as the AI backend here should just extract data.
        #  This was implemented just for the sake of testing.
        ###########################################################

        receipt_data = MongoReceipt(
            user_location="Casablanca",
            user_id=user_id,
            receipt_id=receipt_id,
            purchase_date=datetime.strptime(f"{structured_data.get('date', '1970-01-01')}T{structured_data.get('time', '00:00:00')}", '%Y-%m-%dT%H:%M:%S'),
            items=structured_data.get('items', []),
            total_amount=total_cost,
            currency='MAD'
        )
        receipts_collection.insert_one(receipt_data.dict())

        for item in structured_data.get('items', []):
            purchase_data = MongoPurchase(
                user_id=user_id,
                product_name=item.get('name', 'غير معروف'),
                quantity=item.get('quantity', 1),
                purchase_date=datetime.strptime(f"{structured_data.get('date', '1970-01-01')}T{structured_data.get('time', '00:00:00')}", '%Y-%m-%dT%H:%M:%S'),
                total_amount=item.get('cost', 0) * item.get('quantity', 1)
            )
            purchases_collection.insert_one(purchase_data.dict())

        return jsonify({"status": "success", "data": receipt_data.dict()}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/recommend', methods=['GET'])
def recommend():
    user_id = request.args.get('user_id', "12345")
    days_limit = request.args.get('days', 7)
    recent_purchases = get_recent_purchases(user_id, limit=days_limit)

    for purchase in recent_purchases:
        product = products_collection.find_one({"product_name": purchase["product_name"]})
        if product:
            purchase["category"] = product.get("category", "غير معروف")
            purchase["brand"] = product.get("brand", "غير معروف")
    
    if not recent_purchases:
        return jsonify({"status": "error", "message": "ما كاينش مشتريات حديثة لهذا المستخدم."}), 404

    unique_items = [{"product_name": item['product_name'], "category": item['category']} for item in recent_purchases]
    similar_products, discounts = get_similar_products_and_offers(unique_items)

    items_info = "\n".join([f"{item['product_name']} ({item.get('brand', 'غير معروف')}), المبلغ الإجمالي: {item.get('total_amount', 0)} درهم, الكمية: {item.get('quantity', 0)}" for item in recent_purchases])
    similar_info = "\n".join([f"{', '.join([f'{prod['product_name']} ({prod['brand']}, {prod['category']}) - {prod['price']} درهم في {prod['marketplace']}' for prod in products])}" for products in similar_products])
    discount_info = "\n".join([f"عرض: {offer['offer_details']} - {offer['discount_percentage']}% تخفيض" for offer in discounts])

    user_input = f"""هادو هما العناصر اللي شريتهم في السبع أيام اللي فاتوا:
{items_info}

المنتجات المشابهة اللي لقيتها في الداتا بيز:
{similar_info}

العروض/الخصومات الحالية:
{discount_info}

واش تقدر تعطي نصائح لتوفير الميزانية بناءً على هاد المعلومات، بحال شنو نشري المرة الجاية، شنو نتفادى، وكون دقيق و محدد في الأرقام وكلشي؟"""

    response = conversation.predict(input=user_input)
    print(response)
    return app.response_class(
        response=json.dumps({"status": "success", "recommendation": response}, ensure_ascii=False),
        mimetype='application/json'
    )

system_prompt = """
You are an assistant that provides focused and personalized advice to the user to improve their expenses based on their recent purchases. Clearly outline potential savings and rank them from best to worst. Focus on price comparisons and key differences in pricing for similar products in the same city, mentioning specific marketplaces and available offers. Suggest ways to save money or improve health, such as bulk buying options for frequently purchased items, and align with the user's purchase date. Avoid using general knowledge, and ensure all details are accurate and clearly detailed, with important information in **bold**. Respond only in Moroccan Darija and don't use a single latin letter or word to form any sentence eitheir for market nor brand nor place nor category literally just arabic for all.
"""

chat_prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(system_prompt),
    MessagesPlaceholder(variable_name="chat_history"),
    HumanMessagePromptTemplate.from_template("{input}"),
])  

chat_model = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)
memory = ConversationBufferMemory(return_messages=True, memory_key="chat_history")

conversation = ConversationChain(
    llm=chat_model,
    memory=memory,
    prompt=chat_prompt,
)

if __name__ == '__main__':
    app.run(debug=True)