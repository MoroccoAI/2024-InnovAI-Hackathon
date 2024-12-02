import streamlit as st

def navigate_to(page):
    st.session_state.update({"current_page": page})


import base64

import streamlit as st

def set_background(image_path):
    page_bg_img = f"""
    <style>
    .stApp {{
        background: url({image_path});
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)


# import streamlit as st

# def set_background(image_path):
#     """
#     Set a background image for the Streamlit app.
#     :param image_path: Path to the background image.
#     """
#     page_bg = f"""
#     <style>
#     .stApp {{
#         background: url(data:image/png;base64,{image_path}) no-repeat center center fixed;
#         background-size: cover;
#     }}
#     </style>
#     """
#     st.markdown(page_bg, unsafe_allow_html=True)
