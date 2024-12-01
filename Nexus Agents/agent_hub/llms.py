from langchain_groq import ChatGroq
from langchain_together import ChatTogether
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI

load_dotenv()

def get_llm(provider: str = "groq", model: str = "llama3-70b-8192"):
    """
    Factory function to get different LLM instances.
    
    Args:
        provider: The LLM provider ("groq" or "together")
        model: The model name to use
        
    Returns:
        A configured LLM instance
    """
    if provider == "groq":
        return ChatGroq(model=model)
    elif provider == "together":
        return ChatTogether(model=model)
    elif provider == "mistral":
        return ChatMistralAI(model="pixtral-large-latest")
    else:
        raise ValueError(f"Unsupported provider: {provider}")

# Default instance
groq_llm = get_llm("groq", "llama-3.2-90b-vision-preview")
together_llm = get_llm("together", "meta-llama/Llama-3-70b-chat-hf")
mistral_llm = get_llm("mistral", "pixtral-large-latest")
