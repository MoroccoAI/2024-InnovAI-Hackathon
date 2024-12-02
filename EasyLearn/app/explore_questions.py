import streamlit as st
from model.questions import generate_questions_and_answers
from model.classify import classify_questions
from model.storage import save_outputs
from model.preprocess import extract_and_preprocess_text
from model.inference import generate_embeddings

import streamlit as st
from model.questions import generate_questions_and_answers
from model.classify import classify_questions
from model.storage import save_outputs
from model.preprocess import extract_and_preprocess_text, generate_embeddings  # Correct import




def app():
    st.title("Explore Generated Questions")

    summary = st.session_state.get("summary")
    if not summary:
        st.warning("Please complete the summarization step first.")
        return

    # Ensure text chunks and embeddings are available
    text_chunks = st.session_state.get("text_chunks")
    embeddings = st.session_state.get("embeddings")

    # If not already available, generate text chunks and embeddings
    if not text_chunks or not embeddings:
        text_chunks = extract_and_preprocess_text("data/uploaded_file.pdf")
        embeddings = generate_embeddings(text_chunks)
        st.session_state["text_chunks"] = text_chunks
        st.session_state["embeddings"] = embeddings

    # Generate questions and answers
    questions_and_answers = generate_questions_and_answers(summary, embeddings, text_chunks, min_questions=20)

    # Classify questions
    classified_questions = classify_questions(questions_and_answers)

    # Save results
    save_outputs(None, classified_questions, "data/questions.json")

    # User interaction: choose a difficulty level
    level = st.selectbox("Choose Difficulty Level", ["Basic", "Intermediate", "Advanced"])
    st.subheader(f"{level} Questions")
    for i, qa in enumerate(classified_questions[level.lower()][:5], start=1):
        st.write(f"**Q{i}:** {qa['question']}")
        st.write(f"**A{i}:** {qa['answer']}")
