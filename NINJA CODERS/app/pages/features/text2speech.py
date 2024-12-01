import streamlit as st
import os
from gtts import gTTS
import base64
from io import BytesIO

# Streamlit page configuration
st.set_page_config(page_title="PolyGlot Speech", page_icon="🎙", layout="wide")

# Load the CSS
# with open("pages/styles/style.css") as f:
#     st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Main app container
# Title section
st.markdown("""
    <div style='text-align: center; padding: 2rem 0;'>
        <h1 style='font-size: 3rem;'>🌐 Languito Speech</h1>
        <p style='font-size: 1.2rem; opacity: 0.8;'>Your Advanced Multi-Language Text-to-Speech Platform</p>
    </div>
""", unsafe_allow_html=True)

# Language selection
languages = {
    'en': 'English',
    'fr': 'French',
    'es': 'Spanish',
    'de': 'German',
    'it': 'Italian',
    'ja': 'Japanese',
    'ko': 'Korean',
    'pt': 'Portuguese',
    'nl': 'Dutch',
    'zh-CN': 'Chinese (Simplified)'
}

selected_lang = st.selectbox("Select Language:", list(languages.values()), index=0)
lang_code = [code for code, lang in languages.items() if lang == selected_lang][0]

# Text input
st.markdown(f"### Enter {selected_lang} text:")
input_text = st.text_area("", height=150, max_chars=500, help="Enter the text you want to convert to speech")

# Character and word count
char_count = len(input_text)
word_count = len(input_text.split()) if input_text.strip() else 0
st.text(f"Character count: {char_count} | Word count: {word_count}")

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
    return f'<audio controls autoplay="true"><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>'

# Generate speech button
if st.button("🎙 Generate Speech", type="primary"):
    if input_text.strip():
        with st.spinner("Generating speech..."):
            audio_bytes = text_to_speech(input_text, lang_code)
            if audio_bytes:
                st.markdown("### Generated Speech:")
                st.markdown(get_audio_player(audio_bytes), unsafe_allow_html=True)
                
                # Download button
                st.download_button(
                    label="Download Audio",
                    data=audio_bytes,
                    file_name=f"speech_{lang_code}.mp3",
                    mime="audio/mp3"
                )
    else:
        st.warning("Please enter some text to convert to speech.")

# Additional features
st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    st.markdown("### Features")
    st.info("""
    - High-quality speech synthesis
    - Support for 10 languages
    - Download audio files
    - Real-time character and word counting
    - Modern, user-friendly interface
    """)

with col2:
    st.markdown("### Usage Tips")
    st.success("""
    - For best results, use proper punctuation
    - Keep texts under 500 characters for optimal performance
    - Try different languages to hear the variations
    - Use the download feature to save audio for offline use
    """)

# Footer
st.markdown("---")
st.markdown("Created with ❤ using Streamlit and gTTS")