from transformers import pipeline
from llama_cpp import Llama

# Initialize the Tiny Llama model
llm = Llama(
    model_path="C:/Users/dell/Desktop/e-helth project/tiny-llama-1.1b-chat-medical.fp16.gguf"
)

# Fake patient data template
fake_patient_data = {
    "name": "John Doe",
    "age": 45,
    "gender": "Male",
    "symptoms": ["persistent cough", "fever", "fatigue"],
    "medical_history": ["hypertension", "allergy to penicillin"],
    "current_medications": ["lisinopril", "paracetamol"],
}


# Function to construct the prompt from the message history
def construct_prompt(messages):
    # Include the fake patient data in the initial context
    prompt = f"""
    <|assistant|>
    Patient Profile:
    Name: {fake_patient_data['name']}
    Age: {fake_patient_data['age']}
    Gender: {fake_patient_data['gender']}
    Symptoms: {', '.join(fake_patient_data['symptoms'])}
    Medical History: {', '.join(fake_patient_data['medical_history'])}
    Current Medications: {', '.join(fake_patient_data['current_medications'])}
    </s>\n
    """
    for message in messages:
        if message["role"] == "user":
            prompt += f"<|user|>\n{message['content']}</s>\n"
        elif message["role"] == "assistant":
            prompt += f"<|assistant|>\n{message['content']}</s>\n"
    prompt += "<|assistant|>\n"
    return prompt


# Conversation loop
print(
    "Medical Chatbot - Type your questions below. Type 'exit' to end the conversation."
)
messages = []

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break

    messages.append({"role": "user", "content": user_input})
    prompt = construct_prompt(messages)

    output = llm(prompt, max_tokens=1000, stop=["</s>"])
    response = output["choices"][0]["text"].strip()

    print(f"Assistant: {response}")

    messages.append({"role": "assistant", "content": response})
