import streamlit as st

def app():
    st.title("Answer Questions")

    classified_questions = st.session_state.get("classified_questions")
    if not classified_questions:
        st.warning("Please explore and select questions first.")
        return

    selected_level = st.selectbox("Choose Difficulty Level", ["Basic", "Intermediate", "Advanced"])
    questions = classified_questions[selected_level.lower()][:3]

    responses = {}
    for i, question in enumerate(questions, start=1):
        responses[question["question"]] = st.text_area(f"Answer {i}:", "")

    if st.button("Submit Answers"):
        st.session_state.update({"user_responses": responses})
        st.success("Responses submitted successfully!")
