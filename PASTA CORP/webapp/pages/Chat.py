import json
import streamlit as st
import requests

#maybe
if 'messages' not in st.session_state:
    st.session_state['messages'] = []  

st.markdown(
    """
    <style>
    div[data-testid="stAppViewContainer"] {
        background-color: #F5F7F8;
    }

    section[data-testid="stSidebar"] > div:first-child {
        background-color: #302d34 !important; /* Sidebar background color preserved */
    }

    section[data-testid="stSidebar"] * {
        color: #ffffff !important; /* White text in the sidebar */
    }

    .icon-text {
        display: flex;
        align-items: center;
        margin-bottom: 10px;
        padding: 10px;
        border-radius: 8px;
        transition: background-color 0.3s ease, transform 0.3s ease;
    }

    .icon-text:hover {
        background-color: #444444; /* Background color on hover */
        transform: scale(1.05); /* Zoom effect on hover */
    }

    .icon-text img {
        width: 24px;
        height: 24px;
        margin-right: 8px;
        transition: transform 0.3s ease;
    }

    .icon-text:hover img {
        transform: rotate(15deg); /* Rotation effect on hover */
    }

    .chat-bubble {
        padding: 10px 15px;
        border-radius: 20px;
        margin: 10px 0;
        max-width: 70%;
        word-wrap: break-word;
        display: inline-block;
        transition: transform 0.2s;
    }

    .user-bubble {
        background-color: #007BFF; /* User bubble color */
        color: white;
        text-align: right;
        margin-left: auto;
    }

    .bot-bubble {
        background-color: #E0E0E0; /* Bot bubble color */
        color: black;
        text-align: left;
        margin-right: auto;
    }

    .custom-button {
        padding: 12px 25px;
        font-size: 18px;
        font-weight: bold;
        color: white;
        background: linear-gradient(135deg, #FFD700, #DAA520); /* Gold gradient */
        border: none;
        border-radius: 50px;
        cursor: pointer;
        transition: all 0.3s ease;
        text-align: center;
    }

    .custom-button:hover {
        background: linear-gradient(135deg, #DAA520, #B8860B); /* Darker gold on hover */
        transform: scale(1.05); /* Slight zoom on hover */
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.sidebar.image(
    "assets/Ahmed_xy.png",
     width=300,
     use_container_width=False
)

st.sidebar.markdown(
    """
    <div style="text-align: center; font-weight: bold; font-size: 30px; margin-top: 10px;">
        Découvrez votre Bot Juridique
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown("### Choisissez la spécialité du bot :")

speciality = st.sidebar.selectbox(
    "",
    ["commerce", "travail", "contrats"]
)

st.sidebar.markdown(
    """
    <div class="icon-text">
        <img src="https://cdn-icons-png.flaticon.com/512/11746/11746496.png" alt="Icône Commerce"> 
        <span><b>Commerce</b> : Expertise en droit du commerce.</span>
    </div>
    <div class="icon-text">
        <img src="https://cdn-icons-png.flaticon.com/512/3135/3135715.png" alt="Icône Travail">
        <span><b>Travail</b> : Expertise en droit du travail.</span>
    </div>
    <div class="icon-text">
        <img src="https://cdn-icons-png.flaticon.com/512/4334/4334426.png" alt="Icône Contrats">
        <span><b>Contrats</b> : Expertise en droit des contrats et des obligations.</span>
    </div>
    """,
    unsafe_allow_html=True
)



bot_names = {
    "commerce": "Ahmy - Le Bot Commerce 🤝",
    "travail": "Youssy - Le Bot Travail 💼",
    "contrats": "Samy - Le Bot Contrat ✍️"
}

bot_title = bot_names[speciality]

st.title(bot_title)

user_input = st.text_input("Posez votre question :", key="input")

# if st.markdown(
#     """
#     <button class="custom-button">Envoyer</button>
#     """,
#     unsafe_allow_html=True
# ):
if st.button("Envoyer", key="send_button") and user_input:
    response = requests.post(
        "http://localhost:8000/api/chat", 
        json={"question": user_input, "speciality": speciality}
    )
    
    if response.status_code == 200:
        
        bot_response = response.json().get("answer")
    
    else:
        bot_response = "Je suis désolé, une erreur s'est produite."

    #response = chatbot.get_answer(user_input, speciality)

    # if response:
    #     bot_response = response
    
    # else:
    #     bot_response = "Je suis désolé, une erreur s'est produite."

    st.markdown(
        f"""
        <div class="chat-bubble bot-bubble">{bot_response}</div>
        """,
        unsafe_allow_html=True
    )








