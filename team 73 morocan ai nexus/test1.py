from flask import Flask, request, jsonify
import numpy as np
from pymongo import MongoClient
from transformers import AutoTokenizer, AutoModel
import torch
import google.generativeai as genai
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
CORS(app) 

genai.configure(api_key="AIzaSyAxJmrVLgYfiV2pc3UFMyH2gXjOXgBfjdQ")

client = MongoClient('mongodb://localhost:27017/')
db = client['retrievals'] 
collection = db['data1']  

tokenizer = AutoTokenizer.from_pretrained("CAMeL-Lab/bert-base-arabic-camelbert-msa")
model = AutoModel.from_pretrained("CAMeL-Lab/bert-base-arabic-camelbert-msa")

def vectorize_query(query):
    inputs = tokenizer(query, return_tensors='pt', padding=True, truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).squeeze().numpy()

def cosine_similarity(vec1, vec2):
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

def call_gemini_api(top_answers, user_query):
    prompt = "أنت روبوت دردشة لخدمات المواطنين. بناءً على البيانات التالية:\n"
    for question, answer in top_answers:
        prompt += f"السؤال: {question}\nالإجابة: {answer}\n"
    prompt += f"الرجاء الرد على السؤال التالي: {user_query}\n"
  
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    
    return response.text

def retrieve_answers(user_query, top_n=50):
    query_embedding = vectorize_query(user_query)
    results = collection.find()

    similarities = []
    for doc in results:
        question_embedding = np.array(doc['embedding'])
        similarity = cosine_similarity(query_embedding, question_embedding)
        similarities.append((similarity, doc['question'], doc['answer']))

    similarities.sort(key=lambda x: x[0], reverse=True)
    top_answers = [(question, answer) for _, question, answer in similarities[:top_n]]
    gemini_response = call_gemini_api(top_answers, user_query)

    return top_answers, gemini_response

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    top_answers, gemini_response = retrieve_answers(user_message)

    return jsonify({
        'gemini_response': gemini_response
    })

if __name__ == '__main__':
    app.run(debug=True)
