import openai 
import tiktoken
import os 
import config


## ------------------Chunking the Document --------------###

class TextTokenizer:
    def __init__(self, encoding=config.EMBEDDING_TYPE):
        self.encoding = encoding
        self.tt_encoding = tiktoken.get_encoding(encoding)
    
    def read_file(self,fname):
        with open(fname, 'r', encoding=config.ENCODING) as f:
            file_text = f.read()
        return file_text
    
    def count_tokens(self, text):
        tokens = self.tt_encoding.encode(text)
        return len(tokens)
    
    def creat_chunks(self, text, max_tokens):
        chunks = []
        current_chunk = ""
        current_chunk_tokens = 0
        
        sentences = text.split(".")
        for sentence in sentences:
            sentence_tokens = self.count_tokens(sentence)
            
            # Si l'ajout de la phrase donne as exces de tokens ----> on la rajoute  
            if current_chunk_tokens + sentence_tokens <= max_tokens:
                current_chunk += sentence + "."
                current_chunk_tokens += sentence_tokens

            # Sinon on cree un noveau chunk avec la phrase en cours
            else:
                chunks.append(current_chunk)
                current_chunk = sentence + "."
                current_chunk_tokens = sentence_tokens
        
        if current_chunk:
            chunks.append(current_chunk)
        
        return chunks

