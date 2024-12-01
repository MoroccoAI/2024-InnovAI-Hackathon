import streamlit as st

st.markdown(
    """
    <style>
    div[data-testid="stAppViewContainer"] {
        background-color: #F5F7F8;
    }

    section[data-testid="stSidebar"] > div:first-child {
        background-color: #302d34 !important; /* Couleur originale conservée */
    }

    section[data-testid="stSidebar"] * {
        color: #ffffff !important; /* Assurez que tout le texte de la barre latérale est blanc */
    }

    .service-box {
        background: linear-gradient(135deg, #ffffff, #f8f9fa); /* Gradient background */
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* Subtle shadow */
        text-align: center;
        transition: transform 0.3s, box-shadow 0.3s; /* Smooth hover animation */
    }

    .service-box:hover {
        transform: translateY(-10px); /* Slight upward movement */
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15); /* Stronger shadow on hover */
    }

    .service-header {
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 22px; /* Larger font size */
        font-weight: bold;
        margin-bottom: 15px;
    }

    .service-icon {
        width: 50px; /* Larger icons */
        height: 50px;
        margin-right: 10px;
        border-radius: 50%; /* Circular border for icons */
        border: 2px solid #ddd; /* Light border */
        padding: 5px;
    }

    .service-content {
        font-size: 16px;
        line-height: 1.6;
        margin-top: 10px;
    }

    .stColumn {
        padding: 10px;
    }

    .redirect-button {
        display: flex;
        justify-content: center;
        margin-top: 30px;
    }

    .redirect-button a {
        text-decoration: none;
    }

    .redirect-button button {
        padding: 12px 25px;
        font-size: 18px;
        font-weight: bold;
        color: white;
        background: linear-gradient(135deg, #FFD700, #DAA520); /* Gradient background */
        border: none;
        border-radius: 50px; /* Fully rounded */
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        cursor: pointer;
        transition: all 0.3s ease;
    }

    .redirect-button button:hover {
        background: linear-gradient(135deg, #DAA520, #B8860B); /* Orange Gradient */
        box-shadow: 0 6px 10px rgba(0, 0, 0, 0.2);
        transform: scale(1.05); /* Slight zoom on hover */
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Nos Services")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        <div class="service-box">
            <div class="service-header">
                <img src="https://cdn-icons-png.flaticon.com/512/11746/11746496.png" class="service-icon" alt="Icône Finance">
                Commerce
            </div>
            <div class="service-content">
                Des informations concernant les sociétés commerciales, les transactions commerciales, la gestion des litiges commerciaux, ainsi que la protection des droits de propriété industrielle et intellectuelle.
        </div>
        </div>

        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        """
        <div class="service-box">
            <div class="service-header">
                <img src="https://cdn-icons-png.flaticon.com/512/3135/3135715.png" class="service-icon" alt="Icône Travail">
                Travail
            </div>
            <div class="service-content">
                        Des informations sur les contrats de travail, les droits et obligations des salariés et des employeurs, les conditions de congé, ainsi que les procédures de gestion et de résolution des conflits en milieu professionnel.
        </div>
    </div>

        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        """
        <div class="service-box">
            <div class="service-header">
                <img src="https://cdn-icons-png.flaticon.com/512/4334/4334426.png" class="service-icon" alt="Icône Immobilier">
                Contrats
            </div>
            <div class="service-content">
Des conseils sur la formation, l'exécution et la résiliation des contrats, ainsi que sur les obligations et responsabilités légales des parties contractantes.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown(
    """
    <div class="redirect-button">
        <a href="/Chat" target="_self">
            <button>Démarrer une Conversation</button>
        </a>
    </div>
    """,
    unsafe_allow_html=True
)



