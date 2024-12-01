from agent_hub.llms import mistral_llm, groq_llm
from pydantic import BaseModel

class CLICommand(BaseModel):
    command: str
    description: str

def generate_cli_command(user_input: str, model:str="best", platform:str="windows"):
    if model == "best":
        llm = mistral_llm
    elif model == "fine-tuned":
        llm = groq_llm
    else:
        raise ValueError(f"Unsupported model: {model}")
    llm = llm.with_structured_output(CLICommand)
    prompt = f"""
    You are a CLI command generator. You are given a user input and you need to generate a CLI command that can be executed on a command line interface.
    Platform: {platform}
    User Input: {user_input}
    """
    return llm.invoke(prompt).command