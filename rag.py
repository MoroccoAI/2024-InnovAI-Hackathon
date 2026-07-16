import json
import pinecone
import requests
import numpy as np
import tqdm
import logging
import os

# Configure logging
log_folder = 'log'
os.makedirs(log_folder, exist_ok=True)
log_file = os.path.join(log_folder, 'rag.log')

# Create a custom logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Create handlers
file_handler = logging.FileHandler(log_file, encoding='utf-8')
file_handler.setLevel(logging.INFO)

# Create formatters and add them to handlers
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(file_handler)

# Initialize Pinecone with your API key
with open('apis_keys.json') as f:
    data = json.load(f)
pinecone_api_key = data["pinecone"]["api_key"]
huggingface_api_key = data["huggingface"]["api_key"]

class HuggingFaceEmbedding:
    def __init__(self, model_name='sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'):
        self.model_name = model_name
        self.api_url = f"https://api-inference.huggingface.co/pipeline/feature-extraction/{model_name}"
        self.headers = {
            "Authorization": f"Bearer {huggingface_api_key}",
            "Content-Type": "application/json"
        }
        logger.info(f"\nInitialized HuggingFaceEmbedding with model {model_name}")
    
    def generate_embedding(self, text):
        logger.info(f"\nGenerating embedding for text: {text[:50]}...")
        payload = {
            "inputs": text,
            "options": {"wait_for_model": True}
        }
        
        try:
            response = requests.post(
                self.api_url, 
                headers=self.headers, 
                json=payload
            )
            response.raise_for_status()
            embedding = response.json()
            logger.info("Embedding generated successfully")
            
            return self._normalize_embedding(embedding)
        
        except requests.RequestException as e:
            logger.error(f"Error generating embedding: {e}")
            return None
    
    def _normalize_embedding(self, embedding):
        if isinstance(embedding[0], list):
            embedding = embedding[0]
        
        normalized_embedding = (np.array(embedding) / np.linalg.norm(embedding)).tolist()
        logger.info("Embedding normalized successfully")
        return normalized_embedding

class ArabicRAG:
    def __init__(self, index_name='water-laws', dimension=384):
        self.embedding_model = HuggingFaceEmbedding()
        self.pc = pinecone.Pinecone(api_key=pinecone_api_key)
        self.index_name = index_name
        self.dimension = dimension
        
        try:
            self.pc.create_index(
                name=self.index_name, 
                dimension=self.dimension, 
                metric='cosine'
            )
            logger.info(f"Index {self.index_name} created successfully")
        except Exception as e:
            logger.warning(f"Index may already exist: {e}")
        
        self.index = self.pc.Index(self.index_name)
        logger.info(f"Connected to index {self.index_name}")
    
    def upsert_documents(self, documents):
        logger.info("\nUpserting documents into Pinecone index")
        vectors = []
        for i, doc in enumerate(tqdm.tqdm(documents)):
            embedding = self.embedding_model.generate_embedding(doc)
            
            if embedding is not None:
                vectors.append((
                    f"doc_{i}",
                    embedding,
                    {"text": doc}
                ))
        
        if vectors:
            self.index.upsert(vectors)
            logger.info("Documents upserted successfully")
    
    def retrieve_relevant_context(self, query, top_k=6):
        logger.info(f"Retrieving relevant context for query: {query[:50]}...")
        query_embedding = self.embedding_model.generate_embedding(query)
        
        if query_embedding is None:
            return []
        
        results = self.index.query(
            vector=query_embedding, 
            top_k=top_k,
            include_metadata=True
        )
        
        contexts = [
            result['metadata']['text'] 
            for result in results['matches']
        ]
        
        logger.info(f"Retrieved {len(contexts)} relevant contexts")
        return contexts
    
    def generate_response(self, query):
        logger.info(f"\nGenerating response for query: {query[:50]}...")
        contexts = self.retrieve_relevant_context(query)
        
        response = "السياق ذو الصلة:\n"
        for context in contexts:
            response += f"- {context}\n"
        response += f"\nالسؤال: {query}"
        
        logger.info("Response generated successfully")
        return response

rag = ArabicRAG(index_name='water-laws')

# Read all txt files in the laws/ folder
laws_folder = 'laws'
arabic_documents = []

for filename in os.listdir(laws_folder):
    if filename.endswith('.txt'):
        filepath = os.path.join(laws_folder, filename)
        with open(filepath, 'r', encoding='utf-8') as file:
            arabic_documents.append(file.read())

# rag.upsert_documents(arabic_documents)