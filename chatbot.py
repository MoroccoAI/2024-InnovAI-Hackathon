# -*- coding: utf-8 -*-
import requests
import json
import logging
from rag import ArabicRAG

# Configure logging
logging.basicConfig(filename='log/chatbot.log', level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class AnzarAssistant:
    def __init__(self, api_key: str, model_url: str):
        self.api_key = api_key
        self.model_url = model_url
        logging.info("AnzarAssistant initialized with model URL: %s", model_url)

    def generate_response(self, query: str, context: str) -> str:
        logging.info("Generating response for query: %s", query)
        prompt = f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>أنت أنزار، ملك المياه في الأساطير الأمازيغية، ومساعد ذكي للغاية. أنت تقدم إجابات دقيقة ومفيدة لأسئلة المستخدمين استنادًا إلى السياق المستخرج من القانون المغربي 36-15 المتعلق بالمياه. أنت دائمًا تجيب باللغة العربية فقط. إليك السياق ذي الصلة الذي لديك لاستفسار المستخدم        :
        {context}السؤال:
        {query} الإجابة باللغة العربية:
        <|eot_id|><|start_header_id|>assistant<|end_header_id|>"""

        parameters = {
            "max_new_tokens": 4096,
            "temperature": 0.01,
            "top_k": 50,
            "top_p": 0.95,
            "return_full_text": False
        }

        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

        payload = {
            "inputs": prompt,
            "parameters": parameters
        }

        try:
            response = requests.post(self.model_url, headers=headers, json=payload)
            response.raise_for_status()
            response_text = response.json()[0]['generated_text'].strip()
            logging.info("Response generated successfully")
            return response_text
        except requests.RequestException as e:
            logging.error("Error generating response: %s", str(e))
            return f"Error generating response: {str(e)}"
        

class RAGPipeline:
    def __init__(self, index_name='water-laws', dimension=384, model_url="https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"):
        self.rag = ArabicRAG(index_name=index_name, dimension=dimension)
        logging.info("RAGPipeline initialized with index name: %s and dimension: %d", index_name, dimension)
        
        with open('apis_keys.json') as f:
            data = json.load(f)
            self.huggingface_api_key = data["huggingface"]["api_key"]
        
        self.ansar_assistant = AnzarAssistant(
            api_key=self.huggingface_api_key,
            model_url=model_url
        )

    def process_query(self, query):
        logging.info("Processing query: %s", query)
        contexts = self.rag.retrieve_relevant_context(query, top_k=3)
        
        if not contexts:
            logging.warning("No relevant information found for query: %s", query)
            return "لم يتم العثور على معلومات ذات صلة."

        context_str = "\n".join([f"- {context}" for context in contexts])
        formatted_query = f"السياق ذو الصلة:\n{context_str}\n\nالسؤال: {query}"

        response = self.ansar_assistant.generate_response(formatted_query, context_str)
        
        logging.info("Query processed successfully")
        return response

# # Example usage
# rag_pipeline = RAGPipeline()

# query = "ما هي العقوبات المفروضة على تلوث المياه؟"
# response = rag_pipeline.process_query(query)
# print(response)

# # save the output to a file
# with open("output.txt", "w", encoding="utf-8") as f:
#     f.write(response)