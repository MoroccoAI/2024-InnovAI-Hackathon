import streamlit as st
import requests
import os
from dotenv import load_dotenv
from gtts import gTTS
import base64
from io import BytesIO

# Load environment variables
load_dotenv()

# Hugging Face API setup
API_URL = "https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-{}-{}"
try:
    API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN") or st.secrets["HUGGINGFACE_API_TOKEN"]
except KeyError:
    st.error("Google API Key is not set. Please provide it as an environment variable or in Streamlit secrets.")

headers = {"Authorization": f"Bearer {API_TOKEN}"}

def translate(text, source_lang, target_lang):
    model_url = API_URL.format(source_lang, target_lang)
    payload = {"inputs": text}
    response = requests.post(model_url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()[0]['translation_text']
    else:
        st.error(f"Translation failed. Status code: {response.status_code}")
        return None

def text_to_speech(text, lang):
    try:
        tts = gTTS(text=text, lang=lang, slow=False)
        buf = BytesIO()
        tts.write_to_fp(buf)
        buf.seek(0)
        return buf
    except Exception as e:
        st.error(f"An error occurred during speech synthesis: {str(e)}")
        return None

def get_audio_player(audio_bytes):
    b64 = base64.b64encode(audio_bytes.getvalue()).decode()
    return f'<audio autoplay style="display: none"><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>'

# Initialize session state for audio containers
if 'audio_container_input' not in st.session_state:
    st.session_state.audio_container_input = None
if 'audio_container_output' not in st.session_state:
    st.session_state.audio_container_output = None

# Streamlit app
st.set_page_config(page_title="Languito Translator", page_icon="🌐", layout="wide")

# Title section
st.markdown("""
    <div style='text-align: center; padding: 2rem 0;'>
        <h1 style='font-size: 3rem;'>🌏 Languito Translator</h1>
        <p style='font-size: 1.2rem; opacity: 0.8;'>Your Advanced Language Translation Platform</p>
    </div>
""", unsafe_allow_html=True)

# Language selection
languages = {
    "en": "English",
    "fr": "French",
    "es": "Spanish",
    "de": "German",
    "it": "Italian",
    "ja": "Japanese",
    "zh": "Chinese",
    "ru": "Russian",
    "ar": "Arabic",
    "hi": "Hindi",
    "pt": "Portuguese",
    "nl": "Dutch",
    "ko": "Korean",
    "tr": "Turkish",
    "pl": "Polish",
    "sv": "Swedish"
}

col1, col2 = st.columns(2)

with col1:
    source_lang = st.selectbox("Translate from:", list(languages.values()), index=0, key="source")
    source_code = [code for code, lang in languages.items() if lang == source_lang][0]

with col2:
    target_lang = st.selectbox("Translate to:", list(languages.values()), index=1, key="target")
    target_code = [code for code, lang in languages.items() if lang == target_lang][0]

# Input and output areas side by side
col_input, col_output = st.columns(2)

with col_input:
    st.markdown(f"### Enter {source_lang} text:")
    col1, col2 = st.columns([0.9, 0.1])
    with col1:
        input_text = st.text_area("", height=200, key="input", placeholder="Type or paste your text here...", help="Enter the text you want to translate", max_chars=5000)
    with col2:
        # Create a container for the audio player
        audio_container_input = st.empty()
        if st.button("🔊", key="input_speech", help="Listen to text", kwargs={"className": "speech-button"}):
            if input_text:
                audio_bytes = text_to_speech(input_text, source_code)
                if audio_bytes:
                    audio_container_input.markdown(get_audio_player(audio_bytes), unsafe_allow_html=True)
    char_count = len(input_text)
    word_count = len(input_text.split())
    st.text(f"Character count: {char_count} | Word count: {word_count}")

with col_output:
    st.markdown(f"### Translated {target_lang} text:")
    if 'translated_text' not in st.session_state:
        st.session_state.translated_text = ""

    col3, col4 = st.columns([0.9, 0.1])
    with col3:
        output_placeholder = st.empty()
        output_char_count = st.empty()
    with col4:
        # Create a container for the audio player
        audio_container_output = st.empty()
        if st.button("🔊", key="output_speech", help="Listen to translation", kwargs={"className": "speech-button"}):
            if st.session_state.translated_text:
                audio_bytes = text_to_speech(st.session_state.translated_text, target_code)
                if audio_bytes:
                    audio_container_output.markdown(get_audio_player(audio_bytes), unsafe_allow_html=True)

# Translate button
if st.button("🔄 Translate", type="primary"):
    if input_text:
        try:
            with st.spinner("Translating..."):
                translated_text = translate(input_text, source_code, target_code)
            if translated_text:
                st.session_state.translated_text = translated_text
                output_placeholder.markdown(f'<div class="output-area">{translated_text}</div>', unsafe_allow_html=True)
                output_char_count.text(f"Character count: {len(translated_text)} | Word count: {len(translated_text.split())}")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please enter some text to translate.")

# Additional features
st.markdown("---")
col3, col4 = st.columns(2)

with col3:
    st.markdown("### Recent Updates")
    st.info("""
    - Added text-to-speech functionality for input and output text
    - Added support for more language pairs
    - Improved error handling
    - Enhanced UI with custom styling
    - Added character and word count for both input and output
    """)

with col4:
    st.markdown("### Usage Tips")
    st.success("""
    - For best results, enter clear and complete sentences
    - Maximum recommended length: 5000 characters per translation
    - Supports multiple paragraphs
    - Use the language selection dropdowns to choose your desired languages
    - Click on the speaker icon to hear the text spoken
    """)

