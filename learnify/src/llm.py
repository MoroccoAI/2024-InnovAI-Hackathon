import os
import sys
import keys
import tokenization 
import config

from langchain.document_loaders import TextLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA


class DocumentManager:
    #### --------- Handles loading and chunking of text  ------###

    def __init__(self, filename, encoding=config.EMBEDDING_TYPE):
        self.filename = filename
        self.tokenizer = tokenization.TextTokenizer(encoding)
        self.text = None
        self.chunks = None
    

    def load_document(self):
        #### ------- Loads the document from file -------### 
        self.text = self.tokenizer.read_file(self.filename)

    def split_text(self, max_tokens=config.MAX_TOKENS):
        #### ------- Splits the text into chunks -------### 
        self.chunks = self.tokenizer.creat_chunks(self.text, max_tokens)


class ChunkStore:
    def __init__(self, chunks):
        self.chunks = chunks
        self.vectorestore = None

    def store_chunks(self):
        #### ------- stores the text chunks in a vector database -------###
        texts = [chunk for chunk in self.chunks]
        self.vectorstore = Chroma.from_texts(texts=texts, embedding=OpenAIEmbeddings())

    def retrieve_top_n_chunks(self, question, n=3):
         #### ------- Retrieves the top n relevant chunks for a given question -------###
        important_chunks = self.vectorstore.similarity_search(question)
        return important_chunks[:n]
    
    def get_retriever(self):
        return self.vectorstore.as_retriever()
    
    
class QueryRunner:
    def __init__(self, document_path, model_name=config.MODEL_NAME):
        self.document_path = document_path
        self.model_name = model_name

    def run_query(self, query):
        document_manager = DocumentManager(self.document_path)
        document_manager.load_document()
        document_manager.split_text()
        
        chunk_store = ChunkStore(document_manager.chunks)
        chunk_store.store_chunks()

        chunk_store.retrieve_top_n_chunks(query)

        llm = ChatOpenAI(model_name=self.model_name, temperature=0)
        retriever = chunk_store.vectorstore.as_retriever()
        qa_chain = RetrievalQA.from_chain_type(llm, retriever=retriever)
        response = qa_chain({"query": query})
       
        return response

if __name__ == "__main__":
    os.environ["OPENAI_API_KEY"] = keys.key

    query = sys.argv[1]
    query_runner = QueryRunner(config.DOCUMENT_PATH)
    result = query_runner.run_query(query)
    print(result)
