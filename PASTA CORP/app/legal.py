

import os
import glob
from dotenv import load_dotenv
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS

from openai import OpenAI

import subprocess;
from google.cloud import translate_v2 as translate



load_dotenv()

embeddings = OpenAIEmbeddings()
specialities = ["travail",  "commerce", "contrats"]

def save_faiss_index(speciality):
    with open("data/" + speciality + ".txt", "r", encoding="utf-8-sig") as file:
        data = file.read()
    text_splitter = CharacterTextSplitter(chunk_size=200, chunk_overlap=200)
    chunks = text_splitter.split_text(data)
    faiss_index = FAISS.from_texts(chunks, embeddings)
    faiss_index.save_local( speciality + "_index")

#for speciality in specialities:
 #   save_faiss_index(speciality)

travail_index = FAISS.load_local("travail" + "_index", embeddings, allow_dangerous_deserialization= True)
commerce_index = FAISS.load_local("commerce" + "_index", embeddings, allow_dangerous_deserialization= True)
contrats_index = FAISS.load_local("contrats" + "_index", embeddings, allow_dangerous_deserialization= True)



class Chatbot:

    
    def generate_query_variations(self, query, model="gpt-4"):
        system_prompt = (
            "Tu es un assistant qui génère plusieurs variantes de requêtes pour améliorer les résultats de recherche. "
            "Garde le sens original de la question, mais reformule de manière claire et précise. "
            "Renvoie les variantes sous forme de liste séparée par des sauts de ligne."
        )
        user_prompt = f"Voici la question de l'utilisateur : {query}\nGénère 5 variantes."

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        response = self.openai.chat.completions.create(
            model = "gpt-4o",
            messages = messages
        )
        variations = response.choices[0].message.content.strip().split("\n")
        return variations


    def translate_text(self, text, target_lang):
        print("im here")
        client = translate.Client.from_service_account_json("data/CHANGE.json")

        result = client.translate(text, target_language=target_lang)
        print("now here")

        return result['translatedText']
    
    openai = OpenAI()

    def __init__(self):
        print("Starting the chatbot")

    def generate_answer(self, query: str, speciality: str, system_prompt):
        if(speciality == "travail"):
            index = travail_index
        elif(speciality == "commerce"):
            index = commerce_index
        else:
            index = contrats_index

        query_variations = self.generate_query_variations(query)

        all_results = []

        for variation in query_variations:
            results = index.similarity_search(variation, k=3)  
            all_results.extend(results)

        unique_results = {result.page_content for result in all_results}
        sources_list = list(unique_results)[:4]

        user_prompt = f"Voici la question de l'utilisateur sur le droit du travail: {query}\nvoici les sources que tu dois utiliser pour répondre a cette question: {sources_list}"

        messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        response = self.openai.chat.completions.create(
                    model = "gpt-4o",
                    messages = messages
                )
        
        return {"answer": response.choices[0].message.content,  
                "sources": "\n\n".join(sources_list)}



    def get_answer(self, query: str, speciality: str) -> str:
        system_prompt = "tu dois me dire si la phrase donnée est en marocain ou en français. ne répond qu'avec 'fraçais' ou 'arabe' et aucun autre mot"
        user_prompt = f"Voici la phrase que tu dois classifier: {query}"
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        response_fr_or_ar = self.openai.chat.completions.create(model = "gpt-4o",messages = messages)
        query_language = response_fr_or_ar.choices[0].message.content

        if query_language == "arabe":
            french_query = self.translate_text(query, "ar")
            system_prompt = "Tu es un chatbot assistant conseiller juridique spécialisé en droit du travail marocain. Réponds uniquement sur la base des sources fournies. Si tu ne sais pas ou si les sources ne répondent pas à la question, dis simplement 'Je ne sais pas'. Réponds en arabe."# A la fin de t'as réponses te réécris les soucres données mots pour mots de façon exacte traduites en arabe"
            response = self.generate_answer(french_query, speciality, system_prompt)
            return response["answer"] + \
                    "\nالموارد المستخدمة هي أدناه:\n \n" + \
                    self.translate_text(response["sources"],"ar")

        else: 
            system_prompt = "Tu es un chatbot assistant conseiller juridique spécialisé en droit du travail marocain. Réponds uniquement sur la base des sources fournies. Si tu ne sais pas ou si les sources ne répondent pas à la question, dis simplement 'Je ne sais pas'."
            response = self.generate_answer(query, speciality, system_prompt)
            return response["answer"] + \
                  "\nLes resources utilisée ce trouvent ci-dessous:\n \n" + \
                   response["sources"]
            
