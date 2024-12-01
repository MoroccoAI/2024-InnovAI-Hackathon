import streamlit as st
import random
from gtts import gTTS
from io import BytesIO

# Simple sentence generator
def generate_sentence():
    templates = [
        "The {adjective} {noun} {verb} {adverb}.",
        "{subject} {verb} {object} {adverb}.",
        "In the {place}, {subject} {verb} {object}.",
        "{timeframe}, {subject} will {verb} {object}.",
        "{subject} {verb} {object} because {reason}."
    ]
    
    words = {
        "adjective": ["happy", "sad", "excited", "curious", "friendly", "brave"],
        "noun": ["cat", "dog", "bird", "child", "teacher", "student"],
        "verb": ["runs", "jumps", "sings", "reads", "writes", "plays"],
        "adverb": ["quickly", "slowly", "loudly", "quietly", "carefully", "happily"],
        "subject": ["The boy", "The girl", "The teacher", "The dog", "My friend", "The student"],
        "object": ["the ball", "a book", "the guitar", "homework", "a game", "the puzzle"],
        "place": ["park", "school", "library", "garden", "playground", "museum"],
        "timeframe": ["Tomorrow", "Next week", "In the future", "Soon", "Later today"],
        "reason": ["it's fun", "it's important", "they enjoy it", "it's a hobby", "it's challenging"]
    }
    
    template = random.choice(templates)
    sentence = template.format(**{k: random.choice(v) for k, v in words.items()})
    return sentence

# Function to scramble a sentence into words and add tricky words
def scramble_sentence(sentence):
    words = sentence.lower().split()
    scrambled = words.copy()
    random.shuffle(scrambled)
    
    # Add tricky words
    tricky_words = ["however", "although", "nevertheless", "suddenly", "meanwhile"]
    scrambled.extend(random.sample(tricky_words, 2))
    random.shuffle(scrambled)
    
    return words, scrambled

# Function to generate audio for the sentence
def text_to_speech_quiz(sentence):
    tts = gTTS(text=sentence, lang="en", slow=False)
    buf = BytesIO()
    tts.write_to_fp(buf)
    buf.seek(0)
    return buf

# Streamlit setup
st.title("🎤️ Languito Block Quiz!")
st.markdown("**Listen to the audio and arrange the blocks in the correct order. Watch out for tricky words!**")

# Generate or retrieve a sentence
if "original_sentence" not in st.session_state:
    st.session_state.original_sentence = generate_sentence()

# Generate or retrieve scrambled words
if "correct_words" not in st.session_state or "scrambled_words" not in st.session_state:
    st.session_state.correct_words, st.session_state.scrambled_words = scramble_sentence(st.session_state.original_sentence)

# Play the audio
audio_bytes = text_to_speech_quiz(st.session_state.original_sentence)
st.audio(audio_bytes, format="audio/mp3")

# Display scrambled words as buttons
st.write("### Arrange the words:")
selected_order = st.empty()

selected_words = st.session_state.get("selected_words", [])

# Show buttons for scrambled words
cols = st.columns(4)
for i, word in enumerate(st.session_state.scrambled_words):
    if word not in selected_words:
        if cols[i % 4].button(word, key=word):
            selected_words.append(word)
            st.session_state.selected_words = selected_words

# Display selected words
st.write("### Your sentence:")
st.write(" ".join(selected_words))

# Check the answer
if len(selected_words) == len(st.session_state.correct_words):
    if selected_words == st.session_state.correct_words:
        st.success("🎉 Correct! Great job!")
    else:
        st.error("❌ Incorrect. The correct sentence was: " + " ".join(st.session_state.correct_words))
    
    if st.button("New Quiz"):
        st.session_state.original_sentence = generate_sentence()
        st.session_state.correct_words, st.session_state.scrambled_words = scramble_sentence(st.session_state.original_sentence)
        st.session_state.selected_words = []

# Reset state when user wants a new quiz
if st.button("Reset Quiz"):
    st.session_state.original_sentence = generate_sentence()
    st.session_state.correct_words, st.session_state.scrambled_words = scramble_sentence(st.session_state.original_sentence)
    st.session_state.selected_words = []