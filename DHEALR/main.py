import streamlit as st
import pytesseract
from PIL import Image
import requests
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from llama_cpp import Llama
from googletrans import Translator  # pip install googletrans==4.0.0-rc1
from deep_translator import GoogleTranslator
import base64
import time


def moroccan_design():
    st.markdown(
        """
    <style>
    /* Moroccan Zellige-inspired background with light grey */
    .stApp {
        background-color: #31363F;  /* Grey background */         
        background-size: 40px 40px;
    }
    
    /* Moroccan-style containers with light background */
    .stContainer {
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        padding: 20px;
        margin-bottom: 20px;
    }
    
    /* Moroccan color palette with red and green */
    h1, h2, h3 {
        color: #D32F2F;  /* Red color */
        text-shadow: 1px 1px 2px rgba(211, 47, 47, 0.3);
    }
    
    .stTextInput > div > div > input {
        background-color: #F1F8E9;  /* Light green background */
        border: 2px solid #388E3C;  /* Green border */
        border-radius: 10px;
        color: #388E3C;  /* Green text */
    }
    
    .stButton > button {
        background-color: #388E3C;  /* Green button */
        color: #FFFFFF;  /* White text */
        border-radius: 10px;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background-color: #D32F2F;  /* Red on hover */
        transform: scale(1.05);
    }
    
    /* Moroccan-inspired scroll bar */
    ::-webkit-scrollbar {
        width: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: #E5E5E5;  /* Light grey */
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #388E3C;  /* Green thumb */
        border-radius: 10px;
    }
    
    /* Animation for chat messages */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .chat-message {
        animation: fadeIn 0.5s ease-out;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )


# Cached model loading function (kept the same as original)
@st.cache_resource
def load_models():
    try:
        # Initialize the Tiny Llama model
        llm = Llama(
            model_path="C:/Users/dell/Desktop/e-helth project/tiny-llama-1.1b-chat-medical.fp16.gguf"
        )

        # Initialize the Darija-to-Arabic model
        tokenizer_darija_arabic = AutoTokenizer.from_pretrained(
            "tachicart/nllb-ft-darija"
        )
        model_darija_arabic = AutoModelForSeq2SeqLM.from_pretrained(
            "tachicart/nllb-ft-darija"
        )

        # Initialize the Terjman-Ultra model for Darija translation
        tokenizer_darija = AutoTokenizer.from_pretrained("atlasia/Terjman-Ultra")
        model_darija = AutoModelForSeq2SeqLM.from_pretrained("atlasia/Terjman-Ultra")

        # Initialize the Google Translate API
        translator = Translator()

        return {
            "llm": llm,
            "tokenizer_darija_arabic": tokenizer_darija_arabic,
            "model_darija_arabic": model_darija_arabic,
            "tokenizer_darija": tokenizer_darija,
            "model_darija": model_darija,
            "translator": translator,
        }
    except Exception as e:
        st.error(f"Error loading models: {e}")
        return None


def clean_text(text):
    """Clean the text by replacing <0x0A> with actual newlines."""
    return text.replace("<0x0A>", "\n")


def translate_to_darija(text):
    try:
        translation = GoogleTranslator(source="en", target="ar").translate(text)
        return translation
    except Exception as e:
        return f"Error during translation: {e}"


def translate_to_darija1(text, models):
    """Translate text to Moroccan Darija using Terjman-Ultra model."""
    try:
        inputs = models["tokenizer_darija"](
            text, return_tensors="pt", truncation=True, max_length=512
        )
        outputs = models["model_darija"].generate(**inputs, max_length=512)
        translated_text = models["tokenizer_darija"].decode(
            outputs[0], skip_special_tokens=True
        )
        return clean_text(translated_text)
    except Exception as e:
        st.warning(f"Darija translation error: {e}")
        # Fallback to Google Translate
        try:
            return clean_text(models["translator"].translate(text, dest="ar").text)
        except Exception as fallback_error:
            st.error(f"Fallback translation error: {fallback_error}")
            return text


def translate_darija_to_arabic_to_english(darija_text, models):
    """Translate Darija text to Arabic, then to English."""
    try:
        # Step 1: Translate Darija to Arabic
        inputs = models["tokenizer_darija_arabic"](
            darija_text, return_tensors="pt", truncation=True, max_length=512
        )
        outputs = models["model_darija_arabic"].generate(**inputs, max_length=512)
        arabic_translation = models["tokenizer_darija_arabic"].decode(
            outputs[0], skip_special_tokens=True
        )

        # Step 2: Translate Arabic to English using Google Translate API
        english_translation = (
            models["translator"].translate(arabic_translation, src="ar", dest="en").text
        )

        return {
            "Darija Input": clean_text(darija_text),
            "Arabic Translation": clean_text(arabic_translation),
            "English Translation": clean_text(english_translation),
        }
    except Exception as e:
        st.warning(f"Translation error: {e}")
        try:
            # Fallback to direct Google Translate
            english_translation = (
                models["translator"].translate(darija_text, dest="en").text
            )
            return {
                "Darija Input": clean_text(darija_text),
                "Arabic Translation": "Translation failed",
                "English Translation": clean_text(english_translation),
            }
        except Exception as fallback_error:
            st.error(f"Fallback translation error: {fallback_error}")
            return {
                "Darija Input": clean_text(darija_text),
                "Arabic Translation": "Translation failed",
                "English Translation": clean_text(darija_text),
            }


def construct_prompt(messages):
    """Construct a prompt for the Llama model."""
    prompt = ""
    for message in messages:
        if message["role"] == "user":
            prompt += f"<|user|>\n{message['content']}</s>\n"
        elif message["role"] == "assistant":
            prompt += f"<|assistant|>\n{message['content']}</s>\n"
    prompt += "<|assistant|>\n"
    return prompt


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


def chatbot(models):
    # Apply Moroccan design
    moroccan_design()

    def image_to_base64(image_path):
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
        return encoded_string

    # Base64-encoded image (replace with your own encoded string)
    icon_base64 = image_to_base64("Se7ti.ico")

    # Animated HTML header with Moroccan style
    html_code = f"""
    <div style="display: flex; align-items: center; animation: fadeIn 1s ease-out;">
        <img src="data:image/x-icon;base64,{icon_base64}" width="50" style="margin-right: 10px; transform: rotate(0deg); transition: transform 0.5s ease;">  
        <h1 style="margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.2);">Se7ti AI</h1>
    </div>
    """
    st.markdown(html_code, unsafe_allow_html=True)

    # Add a subtle animation to the subtitle
    st.markdown(
        """
    <div style="animation: fadeIn 1.5s ease-out;">
        <p style="color: #E2DFD0; font-style: italic;">tbib bdarija kijawbk ela l2ass2ila ela se7tk</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Initialize session state for messages
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history with animation
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User input with Moroccan-styled input
    if prompt := st.chat_input("Dkhl So2al diyalk"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)

        # Translate the input
        with st.spinner("Tajma3 l3lougha..."):
            translation_result = translate_darija_to_arabic_to_english(prompt, models)
            translated_input = translation_result["English Translation"]

        # Animated translation details
        with st.expander("Tafassil Tajma3 l3lougha"):
            st.write(f"**Darija Input:** {translation_result['Darija Input']}")
            st.write(
                f"**Arabic Translation:** {translation_result['Arabic Translation']}"
            )
            st.write(f"**English Translation:** {translated_input}")

        # Prepare messages for model
        model_messages = [msg for msg in st.session_state.messages[:-1]] + [
            {"role": "user", "content": translated_input}
        ]

        # Generate response with spinner and animation
        with st.chat_message("assistant"):
            try:
                with st.spinner("Se7ti AI kajawbk..."):
                    # Slight delay to simulate thinking
                    time.sleep(1)

                    # Construct prompt and generate response
                    prompt = construct_prompt(model_messages)
                    output = models["llm"](prompt, max_tokens=500, stop=["</s>"])
                    response = output["choices"][0]["text"].strip()

                    # Translate response to Darija
                    darija_response = translate_to_darija1(response, models)

                    # Animated response
                    st.markdown(darija_response)

                    # Add assistant message to chat history
                    st.session_state.messages.append(
                        {"role": "assistant", "content": response}
                    )

            except Exception as e:
                response = "I'm sorry, I couldn't generate a response."
                st.error(f"Model generation error: {e}")
                st.markdown(response)
                st.session_state.messages.append(
                    {"role": "assistant", "content": response}
                )


def medication_search():
    # Apply Moroccan design
    moroccan_design()

    st.title("Smiyt dwa 🔎")

    # Animated subtitle
    st.markdown(
        """
    <div style="animation: fadeIn 1.5s ease-out;">
        <p style="color: #E2DFD0; font-style: italic;">7et tswera awla dkhl smiyto bach n3tewk tafassil elih .</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Option to choose input method with Moroccan styling
    input_method = st.radio(
        "Khtar wehda mn hado:",
        ("7et Tswera Diyal Dwa", "Dkhl Smiyt Dwa"),
        help="Ikhtar kifash bghiti tdkhol smiyt edwa",
    )

    medicine_name = None

    if input_method == "7et Tswera Diyal Dwa":
        uploaded_image = st.file_uploader(
            "7et Tswera Diyal Dwa", type=["jpg", "png", "jpeg"]
        )
        if uploaded_image is not None:
            # Animated image display
            st.image(
                uploaded_image,
                caption="Uploaded Image",
                use_column_width=True,
                output_format="PNG",
            )
            with st.spinner("Kaynhll smiyt dwa..."):
                medicine_name = extract_medicine_name(uploaded_image)
    elif input_method == "Dkhl Smiyt Dwa":
        medicine_name = st.text_input("Dkhl Smiyt Dwa:")

    if medicine_name:
        # Animated medicine name display
        st.markdown(
            f"""
        <div style="animation: fadeIn 0.7s ease-out; background-color: rgba(139, 69, 19, 0.1); 
        border-left: 5px solid #8B4513; padding: 10px; margin: 10px 0;">
        **Extracted/Entered Medication Name:** {medicine_name}
        </div>
        """,
            unsafe_allow_html=True,
        )

        # Fetch and display drug details with spinner
        with st.spinner("Kayjib l3loughat 3la dwa..."):
            drug_details = fetch_drug_details(medicine_name)
            display_medicine_details(drug_details)
    else:
        st.write("Dkhl hna chi tswera diyal dwa .")


# Main function (similar to original, with design updates)
def main():
    # Set up the Streamlit page with Moroccan-inspired icon
    st.set_page_config(page_title="Se7ti BOT", page_icon="Se7ti.ico")

    # Load models
    models = load_models()
    if not models:
        st.error("kayn chi mouchkil flmodel, 3awd t2eked bila kolchi m9Ad")
        return

    # Sidebar menu with Moroccan styling
    st.sidebar.title("Menu")
    options = st.sidebar.radio(
        "Ikhtar wahd men hadchi:",
        ["Ma3loumat 3la Dawa", "Se7ti BOT"],
        help="Ikhtar l-khedma lli bghiti",
    )

    if options == "Ma3loumat 3la Dawa":
        medication_search()
    elif options == "Se7ti BOT":
        chatbot(models)


if __name__ == "__main__":
    main()
