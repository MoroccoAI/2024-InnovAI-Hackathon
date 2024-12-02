import os
import ollama
import logging
from langchain_ollama import ChatOllama
from langchain_ollama import OllamaEmbeddings
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.retrievers.multi_query import MultiQueryRetriever

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


def create_vector_db(chunks):
    vector_db = Chroma.from_documents(
        documents=chunks,
        embedding=OllamaEmbeddings(model="nomic-embed-text"),
        collection_name="simple-rag",
    )
    logging.info("Vector database created.")
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
    data = ingest_pdf(pdf_doc)
    if data is None:
        return

    chunks = split_documents(data)
    vector_db = create_vector_db(chunks)
    llm = ChatOllama(model="llama3.2")
    retriever = create_retriever(vector_db, llm)
    chain = create_chain(retriever, llm)

    ## We add answers of this Questions to Vector DB
    # question = "What is the document about?"
    # question = "Who is the intended audience for this document?"
    # question = "What questions should I ask the patient based on this document?"
    # question = "What are the key medical terms or diagnoses mentioned in the document?"
    # question = "What medications or treatments are prescribed, including their dosages?"
    # question = "What are the main points as a healthcare assistant I should be aware of?"
    question = "What steps should the healthcare assistant take based on the document's recommendations?"

    # Get the response
    res = chain.invoke(input=question)
    print("Response:")
    print(res)


if __name__ == "__main__":
    main()