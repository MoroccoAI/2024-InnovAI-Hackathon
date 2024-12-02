from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import os

def get_model(model_name: str):
    load_dotenv()
    set_env("OPENAI_API_KEY")
    if model_name == "gpt-4o-mini":
        return ChatOpenAI(model="gpt-4o-mini", temperature=0)
    elif model_name == "gpt-4o":
        return ChatOpenAI(model="gpt-4o", temperature=0)

def set_env(var: str):
    if not os.environ.get(var):
        try:
            os.environ[var] = userdata.get(f"{var}")
        except Exception as e:
            print(f"Error setting environment variable {var}: {e}")
            print(f"Please set {var} manually.")