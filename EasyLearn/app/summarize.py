import streamlit as st
from model.preprocess import extract_and_preprocess_text
from model.inference import generate_segmented_summary
from model.storage import save_outputs

def app():
    st.title("Summarize Your Document")

    if not st.session_state.get("file_uploaded"):
        st.warning("Please upload a PDF on the Home Page first.")
        return

    text_chunks = extract_and_preprocess_text("data/uploaded_file.pdf")
    if not text_chunks:
        st.error("Failed to process the PDF. Please try again.")
        return

    summary = generate_segmented_summary(text_chunks)
    st.text_area("Generated Summary", summary, height=300)
    save_outputs(summary, None, "data/summary.txt")

    if st.button("Proceed to Questions"):
        st.session_state.update({"summary": summary})
