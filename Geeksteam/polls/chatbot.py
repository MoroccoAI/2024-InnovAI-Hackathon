from numpy import outer
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import os
from langdetect import detect
from langchain_groq import ChatGroq
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chains import LLMChain


def detect_language(text):
    try:
        language = detect(text)
        return language
    except:
        return None


load_dotenv(override=True)

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX = os.getenv("PINECONE_INDEX")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
HUGGINGFACE_KEY = os.getenv("HUGGINGFACE_KEY")


pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(PINECONE_INDEX)

model = SentenceTransformer("antoinelouis/biencoder-electra-base-french-mmarcoFR")

llm = ChatGroq(temperature=0, model="llama3-8b-8192", api_key=GROQ_API_KEY)

out_context_french = """Votre phrase est hors contexte, ou manque de clarté ce chatbot est dédié à donner des réponses sur la classification
    de votre infraction au code de la route selon la politique marocaine, veuillez entrer une entrée valide où vous
    expliquez votre amende et je vous renverrai le type d'amende commise."""

out_context_arabic = """عبارتك خارجة عن السياق أو تفتقر إلى الوضوح. هذا المساعد مخصص لتقديم إجابات حول تصنيف 
    مخالفتك لقانون السير وفقًا للسياسة المغربية. يُرجى إدخال معلومات واضحة وصحيحة توضح طبيعة المخالفة 
    وسأقوم بإرجاع نوع المخالفة المرتكبة."""


def preprocess(query):
    embeddings = model.encode(query)
    return [tensor.item() for tensor in embeddings]


def translate_arabic_to_french(arabic_text):
    """
    Translate Arabic text to French using Groq's Llama3 model

    Args:
        arabic_text (str): The Arabic text to be translated

    Returns:
        str: The French translation of the input text
    """
    # Construct a prompt for translation
    translation_prompt = f"""Translate the following Arabic text to French:
    Arabic: {arabic_text}
    
    French Translation:"""

    # Generate the translation
    translation = llm.invoke(translation_prompt).content

    return translation


def predict(query):
    valid = False
    language = detect_language(query)
    if not (language == "fr" or language == "ar"):
        return None, valid, None

    else:
        if language == "ar":
            query = translate_arabic_to_french(query)
        embeddings = preprocess(query)
        result = index.query(vector=embeddings, top_k=1, include_metadata=True)
        print(result)
        score = result["matches"][0]["score"]
        threshold = 0.3
        if float(score) >= threshold:
            valid = True
            return (
                result["matches"][0]["metadata"]["class_violation"],
                valid,
                language,
            )
        else:
            if language == "fr":
                return out_context_french, valid, language
            if language == "ar":
                return out_context_arabic, valid, language


def chain(classes, language, message):
    system_template = """
        Vous êtes un assistant multilingue sophistiqué pour une application de gestion des infractions routières. Votre rôle est de fournir des informations précises et nuancées sur 
        les infractions routières.

        Instructions cruciales :
        - Répondez de manière directe et professionnelle
        - NE PAS mentionner votre processus de réflexion
        - NE PAS ajouter de notes explicatives sur votre ton ou votre style de communication
        - Évitez les formules de politesse artificielle ou les méta-commentaires sur votre réponse
        - Concentrez-vous uniquement sur la communication claire et utile des informations

        - Si le montant de l'amende est supérieur à 0 :
          * Indiquez précisément les délais et montants de paiement
          * Expliquez les conséquences du non-paiement dans les délais

        Critères généraux de communication :
        - Si la langue est français, communiquez entièrement en français
        - Si la langue est arabe, communiquez entièrement en arabe
        - Adaptez le ton et le style de communication à la langue choisie
        - Utilisez une approche empathique et informative
        - Expliquez clairement le type d'infraction, ses implications et les conséquences
        - Intégrez une analyse des sentiments appropriée à la situation

        Objectifs clés :
        1. Fournir des informations précises et contextualisées
        2. Guider l'utilisateur sur les implications de l'infraction
        3. Maintenir un ton respectueux et constructif
        4. Faciliter la compréhension complète de la situation
        """

    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
    # Human question prompt
    human_template = """
                le message d'utilisateur : {input_user}
                Cette amende appartient à la classe : {classe}
                Les points à retirer : {points}
                Montant à payer en cas de règlement immédiat ou dans les 24 heures suivant l`infraction : {montant_immediat}
                Si le règlement est effectué dans les 15 jours suivants : {montant_suivant}
                langue : {language}
                """

    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=llm, prompt=chat_prompt)
    print("retrieved classes from pinecone", classes)
    try:
        response = chain.run(
            input_user=message,
            classe=classes[0],
            points=classes[3],
            montant_immediat=classes[1],
            montant_suivant=classes[2],
            language=language,
        )
        print(response)

        response = response.replace("\n", "<br>")
        return response
    except Exception as e:
        # Handle exceptions gracefully and provide informative feedback
        return f"An error occurred: {str(e)}"
