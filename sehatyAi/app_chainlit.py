from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import ollama
import chainlit as cl

# English -> Darija
english_darija_tokenizer = AutoTokenizer.from_pretrained("atlasia/Terjman-Ultra")
english_darija_model = AutoModelForSeq2SeqLM.from_pretrained("atlasia/Terjman-Ultra")
# english_darija_tokenizer = AutoTokenizer.from_pretrained("atlasia/Terjman-Nano")
# english_darija_model = AutoModelForSeq2SeqLM.from_pretrained("atlasia/Terjman-Nano")

# Darija -> Arabic
darija_arabic_tokenizer = AutoTokenizer.from_pretrained("Saidtaoussi/AraT5_Darija_to_MSA")
darija_arabic_model = AutoModelForSeq2SeqLM.from_pretrained("Saidtaoussi/AraT5_Darija_to_MSA")

# Arabic -> English
arabic_english_tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-ar-en")
arabic_english_model = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-ar-en")

def translate_darija_to_arabic(darija_text):
    darija_tokens = darija_arabic_tokenizer(darija_text, return_tensors="pt", padding=True, truncation=True)
    arabic_output_tokens = darija_arabic_model.generate(**darija_tokens)
    arabic_translation = darija_arabic_tokenizer.decode(arabic_output_tokens[0], skip_special_tokens=True)
    return arabic_translation

def translate_arabic_to_english(arabic_text):
    arabic_tokens = arabic_english_tokenizer(arabic_text, return_tensors="pt", padding=True, truncation=True)
    english_output_tokens = arabic_english_model.generate(**arabic_tokens)
    english_translation = arabic_english_tokenizer.decode(english_output_tokens[0], skip_special_tokens=True)
    return english_translation

def translate_english_to_darija(english_text):
    english_tokens = english_darija_tokenizer(english_text, return_tensors="pt", padding=True, truncation=True)
    darija_output_tokens = english_darija_model.generate(**english_tokens)
    darija_translation = english_darija_tokenizer.decode(darija_output_tokens[0], skip_special_tokens=True)
    return darija_translation

def translate_darija_to_english(darija_text):
    arabic_translation = translate_darija_to_arabic(darija_text)
    english_translation = translate_arabic_to_english(arabic_translation)
    return english_translation

@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set("chat_history", [])

@cl.on_message
async def generate_response(query: cl.Message):
    chat_history = cl.user_session.get("chat_history")
    
    print("Translating Darija input to English...")
    english_query = translate_darija_to_english(query.content)
    print(f"Translated input to English: {english_query}")
    
    chat_history.append({"role": "user", "content": "Answer in 50 words or fewer: " + english_query})
    
    print("Processing query with Ollama...")
    answer = ollama.chat(model="llama3.2", messages=chat_history, stream=True)
    print("Ollama response received.")
    
    complete_answer = ""
    for token_dict in answer:
        token = token_dict["message"]["content"]
        complete_answer += token
    
    print(f"Ollama's English response: {complete_answer}")
    
    print("Translating Ollama's response to Darija...")
    darija_translation = translate_english_to_darija(complete_answer)
    print(f"Darija translation complete: {darija_translation}")
    
    print("Ready !")
    chat_history.append({"role": "assistant", "content": darija_translation})
    cl.user_session.set("chat_history", chat_history)
    print("Sent !")
    
    response = cl.Message(content=darija_translation)
    await response.send()
