from langchain_core.prompts import ChatPromptTemplate

context_check_prompt = """
You are an AI designed to classify user inputs as relevant or not relevant to educational skill extraction and learning-related tasks.
### Task:
1. Analyze the user's input.
2. Determine whether it is relevant to learning, skill development, or educational contexts.
3. Return "Relevant" or "Not Relevant".
### Input:
User Input: [User Input]
### Output:
Return a single string: "Relevant" or "Not Relevant".
"""



def check_relevence_agent(model,query: str):
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", context_check_prompt),
        ("user", "{user_input}")
    ])
    chain = prompt_template | model
    return chain.invoke({"user_input": query}).content
    