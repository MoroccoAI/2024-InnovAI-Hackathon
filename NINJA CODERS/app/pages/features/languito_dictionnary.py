import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
import warnings
import json
from gtts import gTTS
import base64
from io import BytesIO

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Configure Gemini API
genai.configure(api_key=GOOGLE_API_KEY)

# Suppress warnings
warnings.filterwarnings("ignore")

# Streamlit app configuration
st.set_page_config(page_title="Languito Dictionnary", page_icon="📖", layout="wide")

# Language mapping for gTTS
LANGUAGE_CODES = {
    "English": "en",
    "French": "fr", 
    "Spanish": "es", 
    "German": "de", 
    "Italian": "it", 
    "Portuguese": "pt", 
    "Chinese": "zh-CN", 
    "Arabic": "ar", 
    "Russian": "ru", 
    "Darija (Moroccan)": "ar"  # Using Arabic code as closest approximation
}

# Title
st.markdown("""
    <div>
        <h1 class="header-title">📖 Word Context Explorer</h1>
        <p class="header-subtitle">Discover Meanings and Usages with AI</p>
    </div>
""", unsafe_allow_html=True)

# Language selection for input (word language)
input_language = st.selectbox(
    "Select Language for Word Input:",
    list(LANGUAGE_CODES.keys())
)

# Language selection for output (contextual explanation language)
output_language = st.selectbox(
    "Select Language for Output:",
    list(LANGUAGE_CODES.keys())
)

def text_to_speech(text, lang_code):
    """
    Convert text to speech using gTTS
    """
    try:
        # Ensure text is not empty
        if not text or not text.strip():
            return None
        
        tts = gTTS(text=text, lang=lang_code, slow=False)
        buf = BytesIO()
        tts.write_to_fp(buf)
        buf.seek(0)
        return buf
    except Exception as e:
        st.error(f"Audio generation error for '{text}': {str(e)}")
        return None

def get_audio_player(audio_bytes, key=None):
    """
    Create an HTML5 audio player for the generated speech
    """
    if audio_bytes is None:
        return ""
    
    b64 = base64.b64encode(audio_bytes.getvalue()).decode()
    # Add unique key to prevent audio player conflicts
    unique_key = f'key="{key}"' if key else ''
    return f'<audio controls {unique_key}><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>'

def generate_audio_for_content(content, lang_code):
    """
    Generate audio for different content types
    """
    audio_dict = {}
    
    # Check if content is a list or string
    if isinstance(content, list):
        for i, item in enumerate(content):
            if item and item.strip():
                audio = text_to_speech(item, lang_code)
                if audio:
                    audio_dict[f"item_{i}"] = audio
    elif isinstance(content, str) and content.strip():
        audio = text_to_speech(content, lang_code)
        if audio:
            audio_dict["main"] = audio
    
    return audio_dict

def get_word_context(word, input_language, output_language):
    """
    Retrieve contextual information for a given word using Gemini API
    """
    prompt = f"""
    Provide a comprehensive linguistic analysis of the word "{word}" in {input_language}, and return the explanation in {output_language}. Include:
    1. Definition
    2. Parts of Speech
    3. Etymology
    4. 3-4 Example Sentences
    5. Synonyms
    6. Related Words or Nuanced Meanings

    Return the response as a valid JSON string with these keys:
    {{
        "definition": "",
        "parts_of_speech": "",
        "etymology": "",
        "examples": [],
        "synonyms": [],
        "related_words": []
    }}
    """

    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)

        import re
        json_match = re.search(r'\{.*\}', response.text, re.DOTALL)

        if json_match:
            json_str = json_match.group(0)
            return json_str
        else:
            return json.dumps({
                "definition": "Unable to extract structured context.",
                "parts_of_speech": "Unknown",
                "etymology": "Not available",
                "examples": ["No examples could be generated."],
                "synonyms": [],
                "related_words": []
            })
    
    except Exception as e:
        return json.dumps({
            "definition": f"Error retrieving context: {str(e)}",
            "parts_of_speech": "Unknown",
            "etymology": "Not available",
            "examples": ["No examples could be generated."],
            "synonyms": [],
            "related_words": []
        })

# Word input
col1, col2 = st.columns([3, 1])

with col1:
    word_input = st.text_input("Enter a word to explore:", placeholder="Type a word...")

with col2:
    st.write("")  # Spacer
    st.write("")  # Spacer
    context_button = st.button("🔍 Explore", type="primary")

# Context display
if context_button and word_input:
    with st.spinner('Fetching word context...'):
        context_result_str = get_word_context(word_input, input_language, output_language)
    
    try:
        context_result = json.loads(context_result_str)
    except json.JSONDecodeError:
        context_result = {
            "definition": context_result_str,
            "parts_of_speech": "Unknown",
            "etymology": "Not available",
            "examples": ["No examples could be generated."],
            "synonyms": [],
            "related_words": []
        }

    # Determine language code for audio generation from the output language
    audio_lang_code = LANGUAGE_CODES.get(output_language, 'en')

    # Generate audio for various content
    audio_contents = {
        "word": generate_audio_for_content(word_input, audio_lang_code),
        "definition": generate_audio_for_content(context_result.get('definition', ''), audio_lang_code),
        "parts_of_speech": generate_audio_for_content(context_result.get('parts_of_speech', ''), audio_lang_code),
        "etymology": generate_audio_for_content(context_result.get('etymology', ''), audio_lang_code),
        "examples": generate_audio_for_content(context_result.get('examples', []), audio_lang_code),
        "synonyms": generate_audio_for_content(context_result.get('synonyms', []), audio_lang_code),
        "related_words": generate_audio_for_content(context_result.get('related_words', []), audio_lang_code)
    }

    # Display word with audio in the same line but with added space
    st.markdown(f"""
        ### 🔤 Word: 
        <span style='display: flex; align-items: center;'>
            {word_input}
            <span style='margin-left: 10px;'> 
                {get_audio_player(audio_contents['word'].get('main'), 'word') if audio_contents['word'] else ''}
            </span>
        </span>
    """, unsafe_allow_html=True)
    
    # Display the results in card layout
    st.markdown("<div class='card-container'>", unsafe_allow_html=True)

    # Definition Card
    st.markdown(f"""
    <div class='card'>
        <h3>📘 Definition</h3>
        <p>{context_result.get('definition', 'No definition found.')}</p>
        <div style='margin-top: 10px;'>
            {get_audio_player(next(iter(audio_contents['definition'].values()), None), 'definition') if audio_contents['definition'] else ''}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Parts of Speech Card
    st.markdown(f"""
    <div class='card'>
        <h3>📝 Parts of Speech</h3>
        <p>{context_result.get('parts_of_speech', 'Unknown')}</p>
        <div style='margin-top: 10px;'>
            {get_audio_player(next(iter(audio_contents['parts_of_speech'].values()), None), 'parts_of_speech') if audio_contents['parts_of_speech'] else ''}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Example Sentences Card
    st.markdown("""
    <div class='card'>
        <h3>🗣️ Example Usage</h3>
        <ul>
    """, unsafe_allow_html=True)
    
    examples = context_result.get('examples', ['No examples available.'])
    for i, example in enumerate(examples):
        st.markdown(f"""
            <li><span style='display: flex; align-items: center;'>
                {example} 
                <span style='margin-left: 10px;'> 
                    {get_audio_player(audio_contents['examples'].get(f'item_{i}'), f'example_{i}') if audio_contents['examples'] else ''}
                </span>
            </span></li>
        """, unsafe_allow_html=True)
    
    st.markdown("</ul></div>", unsafe_allow_html=True)

    # Etymology Card
    st.markdown(f"""
    <div class='card'>
        <h3>🕰️ Etymology</h3>
        <p>{context_result.get('etymology', 'Etymology not found.')}</p>
        <div style='margin-top: 10px;'>
            {get_audio_player(next(iter(audio_contents['etymology'].values()), None), 'etymology') if audio_contents['etymology'] else ''}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Synonyms Card
    synonyms = context_result.get('synonyms', [])
    if synonyms:
        st.markdown("""
        <div class='card'>
            <h3>📚 Synonyms</h3>
            <p>
        """, unsafe_allow_html=True)
        
        for i, synonym in enumerate(synonyms):
            st.markdown(f"""
                <span style='display: flex; align-items: center;'>
                    {synonym} 
                    <span style='margin-left: 10px;'> 
                        {get_audio_player(audio_contents['synonyms'].get(f'item_{i}'), f'synonym_{i}') if audio_contents['synonyms'] else ''}
                    </span>
                </span>
            """, unsafe_allow_html=True)
        
        st.markdown("</p></div>", unsafe_allow_html=True)
    
    # Related Words Card
    related_words = context_result.get('related_words', [])
    if related_words:
        st.markdown("""
        <div class='card'>
            <h3>🔍 Related Words</h3>
            <p>
        """, unsafe_allow_html=True)
        
        for i, related_word in enumerate(related_words):
            st.markdown(f"""
                <span style='display: flex; align-items: center;'>
                    {related_word} 
                    <span style='margin-left: 10px;'> 
                        {get_audio_player(audio_contents['related_words'].get(f'item_{i}'), f'related_{i}') if audio_contents['related_words'] else ''}
                    </span>
                </span>
            """, unsafe_allow_html=True)
        
        st.markdown("</p></div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

