import os
import ollama
import logging
import streamlit as st
from langchain_ollama import ChatOllama
from langchain_ollama import OllamaEmbeddings
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.retrievers.multi_query import MultiQueryRetriever
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

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

logging.basicConfig(level=logging.INFO)
pdf_doc = "data/World-Health-Organization.pdf"

def ingest_pdf(pdf_doc):
    if os.path.exists(pdf_doc):
        loader = UnstructuredPDFLoader(file_path=pdf_doc)
        data = loader.load()
        logging.info("PDF loaded successfully.")
        return data
    else:
        logging.error(f"PDF file not found at path: {pdf_doc}")
        return None


def split_documents(documents):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=300)
    chunks = text_splitter.split_documents(documents)
    logging.info("Documents split into chunks.")
    return chunks

@st.cache_resource
def load_vector_db():
    embedding = OllamaEmbeddings(model="nomic-embed-text")
    if os.path.exists("./chroma_db"):
        vector_db = Chroma(
            embedding_function=embedding,
            collection_name="simple-rag",
            persist_directory="./chroma_db",
        )
        logging.info("Loaded existing vector database.")
    else:
        data = ingest_pdf(pdf_doc)
        if data is None:
            return None
        chunks = split_documents(data)
        vector_db = Chroma.from_documents(
            documents=chunks,
            embedding=embedding,
            collection_name="simple-rag",
            persist_directory="./chroma_db",
        )
        vector_db.persist()
        logging.info("Vector database created and persisted.")
    return vector_db

def create_retriever(vector_db, llm):
    QUERY_PROMPT = PromptTemplate(
        input_variables=["question"],
        template="""You are an AI language model assistant. Your task is to generate five
different versions of the given user question to retrieve relevant documents from
a vector database. By generating multiple perspectives on the user question, your
goal is to help the user overcome some of the limitations of the distance-based
similarity search. Provide these alternative questions separated by newlines.
Original question: {question}""",
    )

    retriever = MultiQueryRetriever.from_llm(
        vector_db.as_retriever(), llm, prompt=QUERY_PROMPT
    )
    logging.info("Retriever created.")
    return retriever


def create_chain(retriever, llm):
    template = """Answer the question based ONLY on the following context:
{context}
Question: {question}
"""

    prompt = ChatPromptTemplate.from_template(template)

    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    logging.info("Chain created successfully.")
    return chain


def main():
    st.title("مساعدك فالوثائق")
    user_input = st.text_input(":دخل سؤال", "")

    print("Translating Darija input to English...")
    english_query = translate_darija_to_english(user_input)
    print(f"Translated input to English: {english_query}")

    if english_query:
        with st.spinner("Generating response..."):
            try:
                llm = ChatOllama(model="llama3.2")

                vector_db = load_vector_db()
                if vector_db is None:
                    st.error("Failed to load or create the vector database.")
                    return
                retriever = create_retriever(vector_db, llm)
                chain = create_chain(retriever, llm)
                response = chain.invoke(input=user_input)

                print("Translating Ollama's response to Darija...")
                darija_translation = translate_english_to_darija(response)
                print(f"Darija translation complete: {darija_translation}")

                st.markdown("**Assistant:**")
                st.write(darija_translation)
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    else:
        st.info("دخل سؤال باش تبدا")


if __name__ == "__main__":
    main()