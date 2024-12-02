import streamlit as st
from app import home, summarize, explore_questions, answer_questions, results

# Page routing
PAGES = {
    "Home": home.app,
    "Summarization": summarize.app,
    "Explore Questions": explore_questions.app,
    "Answer Questions": answer_questions.app,
    "Results": results.app,
}

def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", list(PAGES.keys()))
    PAGES[page]()

if __name__ == "__main__":
    main()
