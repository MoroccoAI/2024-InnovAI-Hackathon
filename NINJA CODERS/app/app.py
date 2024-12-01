import streamlit as st

  
pages = {
    "Principal": [
        st.Page("pages/home/main.py", title="🏠 Home "),
    ],
    "Activities": [
        st.Page("pages/features/quiz.py", title="📝 Quiz "),
        st.Page("pages/features/block_quiz.py", title="📝 Block Quiz"),
        st.Page("pages/features/languito_chat.py", title="💬 Chat"),
        st.Page("pages/features/languito_translator.py", title="🌏 Translator"),
        st.Page("pages/features/text2speech.py", title="🗣 Prononciation"),
        st.Page("pages/features/languito_dictionnary.py", title="📙 Dictionnary"),
    ],
}

pg = st.navigation(pages)
pg.run()