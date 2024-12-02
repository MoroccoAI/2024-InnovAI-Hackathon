import streamlit as st
from model.evaluation import evaluate_user_responses

def app():
    st.title("Your Results")

    user_responses = st.session_state.get("user_responses", {})
    classified_questions = st.session_state.get("classified_questions", {})

    if not user_responses:
        st.warning("Please submit your answers before proceeding.")
        return

    reference_answers = [q["answer"] for level in classified_questions.values() for q in level]
    scores = evaluate_user_responses(reference_answers, list(user_responses.values()))

    for i, (question, score) in enumerate(zip(user_responses.keys(), scores), start=1):
        st.write(f"**Q{i}: {question}** - Score: {score:.2f}")
