import streamlit as st
import pytesseract
from PIL import Image
import requests
from deep_translator import GoogleTranslator
from llama_cpp import Llama

# Initialize the Tiny Llama model
llm = Llama(
    model_path="C:/Users/dell/Desktop/e-helth project/tiny-llama-1.1b-chat-medical.fp16.gguf"
)

# Fake patient data template
fake_patient_data = {
    "name": "Anas",
    "age": 45,
    "gender": "Male",
    "symptoms": ["persistent cough", "fever", "fatigue"],
    "medical_history": ["hypertension", "allergy to penicillin"],
    "current_medications": ["lisinopril", "paracetamol"],
}


def construct_prompt(messages):
    prompt = (
        "Patient Information:\n"
        f"- Name: {fake_patient_data['name']}\n"
        f"- Age: {fake_patient_data['age']}\n"
        f"- Gender: {fake_patient_data['gender']}\n"
        f"- Symptoms: {', '.join(fake_patient_data['symptoms'])}\n"
        f"- Medical History: {', '.join(fake_patient_data['medical_history'])}\n"
        f"- Current Medications: {', '.join(fake_patient_data['current_medications'])}\n\n"
    )

    for message in messages:
        if message["role"] == "user":
            prompt += f"<|user|>\n{message['content']}</s>\n"
        elif message["role"] == "assistant":
            prompt += f"<|assistant|>\n{message['content']}</s>\n"
    prompt += "<|assistant|>\n"
    return prompt


# Function to modify patient data
def modify_patient_data():
    global fake_patient_data
    st.sidebar.title("Patient Data Management")

    # Display current data
    st.sidebar.write("### Current Patient Data")
    for key, value in fake_patient_data.items():
        st.sidebar.write(f"{key.capitalize()}: {value}")

    option = st.sidebar.selectbox(
        "Choose an action", ["Modify Data", "Delete Data", "Keep Current Data"]
    )

    if option == "Modify Data":
        key = st.sidebar.selectbox("Which field to modify?", fake_patient_data.keys())
        if key in ["symptoms", "medical_history", "current_medications"]:
            new_value = st.sidebar.text_area(
                f"New {key.capitalize()} (comma-separated)",
                value=", ".join(fake_patient_data[key]),
            )
            fake_patient_data[key] = new_value.split(", ")
        else:
            new_value = st.sidebar.text_input(
                f"New {key.capitalize()}", value=fake_patient_data[key]
            )
            fake_patient_data[key] = new_value
        st.sidebar.write(f"{key.capitalize()} updated!")

    elif option == "Delete Data":
        if st.sidebar.button("Delete All Patient Data"):
            fake_patient_data = {
                "name": "",
                "age": "",
                "gender": "",
                "symptoms": [],
                "medical_history": [],
                "current_medications": [],
            }
            st.sidebar.write("Patient data deleted!")

    return fake_patient_data


# Function to handle chatbot interaction
def chatbot():
    st.title("Medical Chatbot")
    st.write(
        "Ask your medical-related questions below. The chatbot is ready to assist you!"
    )

    # Session state for conversation history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    user_input = st.text_input("You:", key="chat_input")
    if user_input:
        # Append user message to the history
        st.session_state.messages.append({"role": "user", "content": user_input})
        prompt = construct_prompt(st.session_state.messages)

        # Generate chatbot response
        output = llm(prompt, max_tokens=500, stop=["</s>"])
        response = output["choices"][0]["text"].strip()
        response = response.replace("<0x0A>", "\n").strip()
        # Append assistant response to the history
        st.session_state.messages.append({"role": "assistant", "content": response})

    # Display conversation history
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.write(f"You: {message['content']}")
        elif message["role"] == "assistant":
            st.write(f"Assistant: {message['content']}")


# Function to extract the name of the medication from an image using OCR
def extract_medicine_name(image_path):
    img = Image.open(image_path)
    extracted_text = pytesseract.image_to_string(img)
    lines = extracted_text.split("\n")
    medicine_name = ""
    for line in lines:
        line = line.strip()
        if line and line.isupper() and not any(char.isdigit() for char in line):
            medicine_name = line
            break
    if not medicine_name:
        for line in lines:
            if line.strip():
                medicine_name = line.strip()
                break
    return medicine_name


# Function to fetch drug details from the OpenFDA API
def fetch_drug_details(medicine_name):
    OPENFDA_API_URL = "https://api.fda.gov/drug/label.json"
    try:
        response = requests.get(
            f"{OPENFDA_API_URL}?search=openfda.brand_name:{medicine_name}&limit=1"
        )
        data = response.json()
        if "results" in data and data["results"]:
            drug_info = data["results"][0]
            name = drug_info.get("openfda", {}).get("brand_name", ["N/A"])[0]
            purpose = drug_info.get("purpose", ["N/A"])[0]
            warnings = drug_info.get("warnings", ["N/A"])[0]
            side_effects = drug_info.get("adverse_reactions", ["N/A"])[0]
            dosage = drug_info.get("dosage_and_administration", ["N/A"])[0]
            return {
                "name": name,
                "purpose": purpose,
                "warnings": warnings,
                "side_effects": side_effects,
                "dosage": dosage,
            }
        else:
            return "No information available for this medication."
    except Exception as e:
        return f"Error fetching data: {e}"


# Function to translate text to Moroccan Darija (Arabic) using deep_translator
def translate_to_darija(text):
    try:
        translation = GoogleTranslator(source="en", target="ar").translate(text)
        return translation
    except Exception as e:
        return f"Error during translation: {e}"


# Function to display and structure the fetched data
def display_medicine_details(details):
    if isinstance(details, dict):
        name = translate_to_darija(f"Medicine Name: {details['name']}")
        purpose = translate_to_darija(f"Purpose: {details['purpose']}")
        warnings = translate_to_darija(f"Warnings: {details['warnings']}")
        side_effects = translate_to_darija(f"Side Effects: {details['side_effects']}")
        dosage = translate_to_darija(f"Dosage: {details['dosage']}")

        st.write(f"### {name}")
        st.write(f"**{purpose}**")
        st.write(f"**{warnings}**")
        st.write(f"**{side_effects}**")
        st.write(f"**{dosage}**")
    else:
        st.write(details)


# Function to handle medication search
def medication_search():
    st.title("Medication Information Extractor")
    st.write(
        "Upload an image of the medication or enter its name to get details like purpose, warnings, side effects, etc."
    )

    # Option to choose input method
    input_method = st.radio(
        "Select input method:", ("Upload Image", "Enter Medication Name")
    )

    medicine_name = None

    if input_method == "Upload Image":
        uploaded_image = st.file_uploader(
            "Choose an image of the medication", type=["jpg", "png", "jpeg"]
        )
        if uploaded_image is not None:
            st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)
            medicine_name = extract_medicine_name(uploaded_image)
    elif input_method == "Enter Medication Name":
        medicine_name = st.text_input("Enter the name of the medication:")

    if medicine_name:
        st.write(f"**Extracted/Entered Medication Name:** {medicine_name}")
        # Fetch and display drug details
        drug_details = fetch_drug_details(medicine_name)
        display_medicine_details(drug_details)
    else:
        st.write("Please provide a medication name or upload an image.")


# Main app with menu
def main():
    st.sidebar.title("Menu")
    options = st.sidebar.radio(
        "Choose an option:",
        ["Medication Search", "Medical Chatbot", "Manage Patient Data"],
    )

    if options == "Medication Search":
        medication_search()
    elif options == "Medical Chatbot":
        modify_patient_data()  # Allow user to modify patient data
        chatbot()
    elif options == "Manage Patient Data":
        modify_patient_data()  # Allow user to manage patient data directly


if __name__ == "__main__":
    main()
