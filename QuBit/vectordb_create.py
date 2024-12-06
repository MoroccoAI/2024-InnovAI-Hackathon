import json
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document

# Paths
DATA_PATH = 'deduplicated_dataset.json'
DB_FAISS_PATH = 'vectorstore/db_faiss'

def load_json_dataset(file_path):
    """
    Load JSON dataset and convert to LangChain Documents
    
    Each document will combine instruction, input, output, and category
    to create a comprehensive searchable text
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    documents = []
    for item in data:
        # Combine all relevant fields into a single text
        text = f"Instruction: {item.get('instruction', '')}\n" \
               f"Input: {item.get('input', '')}\n" \
               f"Output: {item.get('output', '')}\n" \
               f"Category: {item.get('category', '')}"
        
        # Create a LangChain Document
        doc = Document(
            page_content=text,
            metadata={
                'source': 'morocco_tourism_dataset',
                'category': item.get('category', ''),
                'original_instruction': item.get('instruction', '')
            }
        )
        documents.append(doc)
    
    return documents

def create_vector_db():
    """
    Create a FAISS vector database from the JSON dataset
    """
    # Load documents from JSON
    documents = load_json_dataset(DATA_PATH)
    
    # Text splitter to chunk documents
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    
    # Split documents into smaller chunks
    texts = text_splitter.split_documents(documents)
    
    # Initialize embeddings
    embeddings = HuggingFaceEmbeddings(
        model_name='sentence-transformers/all-MiniLM-L6-v2',
        model_kwargs={'device': 'cpu'}
    )
    
    # Create FAISS vector store
    try:
        db = FAISS.from_documents(texts, embeddings)
        
        db.save_local(DB_FAISS_PATH)
        print(f"Vector database successfully created and saved to {DB_FAISS_PATH}")
    
    except Exception as e:
        print(f"Error creating vector database: {e}")

def load_vector_db():
    """
    Optional method to load an existing vector database
    """
    embeddings = HuggingFaceEmbeddings(
        model_name='sentence-transformers/all-MiniLM-L6-v2',
        model_kwargs={'device': 'cpu'}
    )
    
    try:
        db = FAISS.load_local(DB_FAISS_PATH, embeddings)
        return db
    except Exception as e:
        print(f"Error loading vector database: {e}")
        return None

if __name__ == "__main__":
    import os
    os.makedirs('vectorstore', exist_ok=True)
    
    # Create the vector database
    create_vector_db()
