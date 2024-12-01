from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

template = """
Answer the question below.

Here is the conversation history: {context}

Question: {question}

Answer:
"""

model = OllamaLLM(model="llama3.2")

prompt = ChatPromptTemplate.from_template(template)


custom_prompt = """
    Give me an alternative medication to Doliprane 1000mg in Morocco. The alternative medication should figure in the following list of medications: 
    Ibuprofen 400mg (Brufen, Nurofen), Aspirin 500mg (Bayer, Aspegic), Naproxen 250mg (Aleve, Naprosyn), Paracetamol 500mg (Panadol, Efferalgan), 
    Diclofenac Sodium 25mg (Voltaren, Cataflam), Tramadol 50mg (Ultram, Tramal), Codeine 30mg (Codipar, Co-Codamol), Ketoprofen 25mg (Oruvail, Actron), 
    Meloxicam 15mg (Mobic), Diclofenac + Misoprostol 50mg (Arthrotec).
    """
# Correctly construct the chain
def handle_conversation(context, question):
    context = ""
    print("Welcome to the AI chatbot assistant by pharmaIQ")
     
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        # Format the input using the prompt template
        formatted_input = prompt.format(context=context, question=user_input)
        # Invoke the model with the formatted input
        result = model.invoke(formatted_input)
        print("AI: ", result)
        context += f"You: {user_input}\nAI: {result}\n"

if __name__ == "__main__":
   
    handle_conversation("", custom_prompt)