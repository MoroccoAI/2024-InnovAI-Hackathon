
import streamlit as st
st.set_page_config(page_title="Chatbot IA Juridique Marocain", layout="wide")
import os


st.markdown(
    """
    <style>
    h1, h2, h3 {
        color: #2c3e50;
        font-family: 'Arial', sans-serif;
    }
    p {
        font-size: 16px;
        color: #4d4d4d;
    }

    [data-testid="stSidebar"] {
        background-color: #302d34; /* Sidebar dark background */
    }
    [data-testid="stSidebar"] * {
        color: #ffffff !important; /* Ensure white text */
    }
    [data-testid="stSidebar"] a {
        color: #00c8ff; /* Custom link color in sidebar */
    }

    div[data-testid="stAppViewContainer"] {
        background-color: #F5F7F8; /* Light gray background for main area */
    }

    .info-box {
        background: linear-gradient(135deg, #ffffff, #f8f9fa); /* Subtle gradient */
        border-radius: 15px;
        padding: 20px;
        margin: 20px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    .info-box:hover {
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
        transform: translateY(-5px); /* Slight upward motion */
        transition: all 0.3s ease;
    }

    .cta-button {
        display: flex;
        justify-content: center;
        margin-top: 30px;
    }

    .cta-button a {
        text-decoration: none;
    }

    .cta-button button {
        padding: 12px 25px;
        font-size: 18px;
        font-weight: bold;
        color: white;
        background: linear-gradient(135deg, #FFD700, #DAA520); /* Gold Gradient */
        border: none;
        border-radius: 50px; /* Fully rounded */
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        cursor: pointer;
        transition: all 0.3s ease;
    }

    .cta-button button:hover {
        background: linear-gradient(135deg, #DAA520, #B8860B); /* Darker gold on hover */
        box-shadow: 0 6px 10px rgba(0, 0, 0, 0.2);
        transform: scale(1.05); /* Slight zoom on hover */
    }

    .content-icon {
        width: 20px;
        height: 20px;
        margin-right: 10px;
        vertical-align: middle;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        background-color: #302d34; /* Sidebar color */
    }

    [data-testid="stSidebar"] * {
        color: #ffffff !important;
    }

    [data-testid="stSidebar"] a {
        color: #00c8ff;
    }
    </style>
    """,
    unsafe_allow_html=True
)

flag_path = "assets/morocco_flag.png"

with st.container():
    if os.path.exists(flag_path):
        st.image(flag_path, width=150) 
    else:
        st.error("Flag image not found. Please check the file path.")
    st.markdown("<h1 style='margin-top: -10px;'>Chatbot IA Juridique Marocain</h1>", unsafe_allow_html=True)

st.markdown(
    """
    <div class="info-box">
        <h2>Bienvenue !</h2>
        <p>
        Bienvenue sur l'application <strong>Chatbot IA Juridique Marocain</strong> !
        Découvrez une plateforme moderne et intelligente, alimentée par l'intelligence artificielle, offrant des conseils juridiques rapides et accessibles.
        Que vous soyez à la recherche d'informations sur le droit des obligations et des contrats, le droit du travail, ou le droit commercial, notre chatbot est là pour vous fournir des réponses claires et adaptées à vos besoins.
        </p>
    </div>

    <div class="info-box">
        <h2>Comment utiliser l'application</h2>
        <ol>
            <li><img src="https://cdn-icons-png.flaticon.com/512/1946/1946433.png" alt="Accueil Icon" class="content-icon"> <strong>Accueil</strong> : Découvrez notre mission et nos services principaux.</li>
            <li><img src="https://cdn-icons-png.flaticon.com/512/2076/2076538.png" alt="Chat Icon" class="content-icon"> <strong>Chat</strong> : Posez vos questions directement à notre chatbot et recevez des réponses instantanées.</li>
            <li><img src="https://cdn-icons-png.flaticon.com/512/13330/13330989.png" alt="Services Icon" class="content-icon"> <strong>Services</strong> : Parcourez les solutions juridiques que nous proposons.</li>
            <li><img src="https://cdn-icons-png.flaticon.com/512/1533/1533223.png" alt="À propos de nous Icon" class="content-icon"> <strong>À propos de nous</strong> : Apprenez-en plus sur notre équipe.</li>
        </ol>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="cta-button">
        <a href="/Services" target="_self">
            <button>Explorez nos Services</button>
        </a>
    </div>
    """,
    unsafe_allow_html=True
)
