import os
import sys
import torch
import chainlit as cl
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_community.llms import CTransformers

# Set encoding to UTF-8
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

# Paths
DB_FAISS_PATH = 'vectorstore/db_faiss'
LLM_PATH = 'llama-2-7b-chat.ggmlv3.q8_0.bin'

# Custom Prompt Template
custom_prompt_template = """You are an AI assistant specializing in Morocco tourism. 
Use the provided context to answer the user's question concisely and coherently. Avoid repetition or adding information not found in the context. 

Context: {context}

Question: {question}

Provide a clear and helpful response:
"""

def set_custom_prompt():
    prompt = PromptTemplate(
        template=custom_prompt_template,
        input_variables=['context', 'question']
    )
    return prompt

def load_llm():
    """
    Load the GGML model using CTransformers
    """
    try:
        if not os.path.exists(LLM_PATH):
            print(f"Error: Model file not found at {LLM_PATH}")
            print("Current directory contents:", os.listdir())
            return None
        
        # Load the model
        llm = CTransformers(
            model=LLM_PATH,
            model_type="llama",
            max_new_tokens=512,
            temperature=0.5,
            top_p=0.8,
            repetition_penalty=1.1
        )
        return llm
    
    except Exception as e:
        print(f"Error loading LLM: {e}")
        import traceback
        traceback.print_exc()
        return None

def retrieval_qa_chain(llm, prompt, db):
    """
    Create a Retrieval QA Chain
    """
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type='stuff',
        retriever=db.as_retriever(
            search_kwargs={
                'k': 3,
                'search_type': 'similarity'
            }
        ),
        return_source_documents=True,
        chain_type_kwargs={'prompt': prompt}
    )
    return qa_chain

def qa_bot():
    """
    Initialize QA Bot with embeddings, vector store, and LLM
    """
    try:
        # Load embeddings
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'}
        )
        
        # Verify vector store path exists
        if not os.path.exists(DB_FAISS_PATH):
            print(f"Error: Vector store path not found: {DB_FAISS_PATH}")
            print("Current directory contents:", os.listdir())
            return None
        
        # Load vector store
        try:
            db = FAISS.load_local(
                DB_FAISS_PATH, 
                embeddings,
                allow_dangerous_deserialization=True
            )
        except Exception as db_error:
            print(f"Error loading vector store: {db_error}")
            import traceback
            traceback.print_exc()
            return None
        
        # Load LLM
        llm = load_llm()
        if not llm:
            print("Error: Could not load language model")
            return None
        
        # Set custom prompt
        qa_prompt = set_custom_prompt()
        
        # Create QA chain
        qa = retrieval_qa_chain(llm, qa_prompt, db)
        
        return qa
    
    except Exception as e:
        print(f"Error setting up QA bot: {e}")
        import traceback
        traceback.print_exc()
        return None

##############################################
# Chainlit Chat Interface
@cl.on_chat_start
async def start():
    """
    Initialize the chatbot when a new chat starts
    """
    # Send loading message
    msg = cl.Message(content="Initializing Morocco Tourism Chatbot...")
    await msg.send()
    
    try:
        # Setup QA chain
        chain = qa_bot()
        if not chain:
            await cl.Message(content="Failed to initialize the chatbot. Please check your setup.").send()
            return
        
        # Store chain in user session
        cl.user_session.set("chain", chain)
        
        # Welcome message
        await cl.Message(content="Salam! Welcome to the Morocco Tourism Chatbot! Ask me anything about traveling in Morocco.").send()
    
    except Exception as e:
        print(f"Detailed Initialization Error: {e}")
        import traceback
        traceback.print_exc()
        await cl.Message(content=f"Error during initialization: {str(e)}").send()

# @cl.on_message
# async def main(message: cl.Message):
#     """
#     Process incoming messages
#     """
#     # Retrieve the QA chain
#     chain = cl.user_session.get("chain")
    
#     # Create a callback handler for streaming
#     cb = cl.AsyncLangchainCallbackHandler(
#         stream_final_answer=True,
#         answer_prefix_tokens=["FINAL", "ANSWER"]
#     )
#     cb.answer_reached = True
    
#     try:
#         # Process the query
#         res = await chain.acall(message.content, callbacks=[cb])
#         answer = res["result"]
#         sources = res.get("source_documents", [])
        
#         # Prepare response with sources
#         if sources:
#             source_texts = "\n\n".join([
#                 f"Source {i+1}: {doc.page_content}" 
#                 for i, doc in enumerate(sources)
#             ])
#             full_response = f"{answer}\n\n**Sources:**\n{source_texts}"
#         else:
#             full_response = f"{answer}\n\n*No specific sources found.*"
        
#         # Send the response
#         await cl.Message(content=full_response).send()
    
#     except Exception as e:
#         print(f"Detailed Query Processing Error: {e}")
#         import traceback
#         traceback.print_exc()
#         await cl.Message(content=f"Error processing your query: {str(e)}").send()
@cl.on_message
async def main(message: cl.Message):
    """
    Process incoming messages
    """
    # Retrieve the QA chain
    chain = cl.user_session.get("chain")
    
    # Create a callback handler for streaming
    cb = cl.AsyncLangchainCallbackHandler(
        stream_final_answer=True,
        answer_prefix_tokens=["FINAL", "ANSWER"]
    )
    cb.answer_reached = True
    
    try:
        # Process the query
        res = await chain.acall(message.content, callbacks=[cb])
        answer = res["result"]
        
        # Truncate if the answer seems cut off
        if answer.endswith('Marrak'):
            answer = answer.rstrip('Marrak')
        
        # Remove repetitive information
        lines = answer.split('\n')
        unique_lines = []
        seen = set()
        for line in lines:
            if line not in seen:
                unique_lines.append(line)
                seen.add(line)
        
        answer = '\n'.join(unique_lines)
        
        await cl.Message(content=answer).send()
    
    except Exception as e:
        print(f"Detailed Query Processing Error: {e}")
        import traceback
        traceback.print_exc()
        await cl.Message(content=f"Error processing your query: {str(e)}").send()
