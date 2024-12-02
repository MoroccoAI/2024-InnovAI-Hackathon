
from pdfminer.high_level import extract_text
from sentence_transformers import SentenceTransformer
import re
import numpy as np
import faiss

# def extract_and_preprocess_text(pdf_path, chunk_size=500):
#     raw_text = extract_text(pdf_path)
#     clean_text = re.sub(r"\s+", " ", raw_text.replace("\n", " ")).strip()
#     return [clean_text[i:i + chunk_size] for i in range(0, len(clean_text), chunk_size)]


def extract_and_preprocess_text(pdf_path, chunk_size=500):
    """
    Extract and preprocess text from a PDF.
    """
    try:
        raw_text = extract_text(pdf_path)
        if not raw_text.strip():
            raise ValueError("The PDF contains no readable text.")
        clean_text = re.sub(r"\s+", " ", raw_text.replace("\n", " ")).strip()
        text_chunks = [clean_text[i:i + chunk_size] for i in range(0, len(clean_text), chunk_size)]
        return text_chunks
    except Exception as e:
        print(f"Error extracting text: {e}")
        return []

def generate_embeddings(text_chunks):
    """
    Generate embeddings for text chunks.
    """
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(text_chunks)
    return embeddings

def store_embeddings(embeddings):
    """
    Store embeddings in a FAISS index.
    """
    embedding_dim = len(embeddings[0])
    index = faiss.IndexFlatL2(embedding_dim)
    index.add(np.array(embeddings))
    return index


