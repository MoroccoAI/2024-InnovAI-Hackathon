import streamlit as st
st.set_page_config(page_title="À propos de nous", layout="wide")

# Configure the page

st.markdown(
    """
    <style>
    h1, h2, h3 {
        color: #2c3e50; /* Dark gray-blue for headers */
        font-family: 'Arial', sans-serif;
    }
    p {
        font-size: 16px; /* Slightly larger font for readability */
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
    </style>
    """,
    unsafe_allow_html=True
)

st.title("À propos de nous")

st.markdown(
    """
    <div class="info-box">
        <h2>Qui sommes-nous ?</h2>
        <p>
            Nous sommes une équipe de cinq amis passionnés par l'innovation et l'informatique, à la recherche de challenge pour gagner de l'experience.
            Nous avons décidé de participer au Hackathon MoroccoAI. Motivés par cette opportunité, nous avons travaillé sans relaches pour finir le projet.
                  </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="info-box">
        <h2>Notre mission</h2>
            En analysant les sujets proposés par les mentors et en identifiant un besoin évident d’accès simplifié à des informations juridiques fiables au Maroc,
            nous avons orienté notre solution vers trois domaines:
            <ul>
            <li>Le droit du commerce</li>
            <li>Le droit des obligations et des contrats</li>
            <li>Le droit du travail</li>
        </ul>
            Nos chatbots Ahmy, Youssy et Samy sont conçus pour vous assister avec précision dans vos questionnements juridiques.
            Que vous soyez un particulier, un étudiant ou un professionnel, nos chatbots sont là pour vous accompagner et vous donner des réponses adaptées à vos besoins.
            
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="info-box">
        <h2>Notre équipe</h2>
        <p>
            Derrière notre application <b>Chatbot IA Juridique Marocain</b>, se trouvent cinq amis passionnés:
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.image("assets/All_Might_image.jpg", caption="Taha El Hihi", use_container_width=True)

with col2:
    st.image("assets/Endeavor_image.jpg", caption="Andreas Salice", use_container_width=True)

with col3:
    st.image("assets/Night_eye_image.jpg", caption="Pascalis Felahidis", use_container_width=True)

with col4:
    st.image("assets/Mirio_image.jpg", caption="Samy Sidki", use_container_width=True)

with col5:
    st.image("assets/minoru_image.jpg", caption="Ayman Zeriouh", use_container_width=True)




