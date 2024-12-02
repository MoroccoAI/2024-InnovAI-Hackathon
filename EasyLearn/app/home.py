import streamlit as st
from app.utils import set_background



def app():
    # try:
    #     from app.utils import set_background
    #     print("set_background function imported successfully!")
    # except ImportError as e:
    #     print(f"ImportError: {e}")
    #set_background("D:/AIstuff/moroccoAI/MOROCCANAIhackathon/data/baig.webp")
    set_background("data/baig.webp")  
    st.title("Welcome to the AI-Powered Learning Assistant")
     # Ensure the path is correct
    st.markdown(
        """
        ## Upload your PDF
        - Upload a PDF to extract and summarize content.
        - Explore questions generated from the content.
        - Test your understanding with interactive Q&A.
        """
    )
    pdf_file = st.file_uploader("Upload your PDF", type=["pdf"])
    if pdf_file:
        with open("data/uploaded_file.pdf", "wb") as f:
            f.write(pdf_file.read())
        st.success("File uploaded successfully!")
        st.button("Proceed to Summarization", on_click=lambda: st.session_state.update({"file_uploaded": True}))
    
    