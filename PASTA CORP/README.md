# AI-Powered Moroccan Legal Advisor Chatbot

An AI chatbot, accessible through a web interface, capable of finding information for legal inquiries and sharing the relevant sources.

---

## 📖 Background and Problem Statement

Finding information for common legal inquiries is not always easy. Moreover, consulting a professional for small problems can be expensive and time-consuming.

---

## 🌟 Impact and Proposed Solution

Our goal is to make legal information accessible to the broad public trough AI and assist law students in an innovative way. 

---

## 🏆 Evaluation

The chatbot has been tested by and positively surprised a Moroccan PhD student in Law, who praised its potential as an educational resource for law students.

---

## 📋 Project Outcomes and Deliverables

### Deliverables:
1. **`app` folder**  
   Contains the codebase for the RAG-based chatbot backend.
2. **`webapp` folder**  
   Frontend implementation developed using Streamlit.
3. **`LegalChatbot_powerpoint.pdf`**  
   Comprehensive pitch slides detailing the project's concept and execution.
4. **Demo, Pitch, and Deployed Version Links**  
   - **[https://drive.google.com/file/d/1fRjFgSFqIMs_puP9ooiigPC4E8m448FH/view?usp=sharing](#)**  
   - **[https://drive.google.com/file/d/1cYWuleys9mi7UUKLFhkli-f2s3Ek29tV/view?usp=sharing](#)**  
   - **[https://moroccolawchatbot-zaevffgycsnvdvtsijkok7.streamlit.app/Chat](#)**

---

## 📚 Data Sources

The chatbot utilizes structured legal data from the following Moroccan legal codes:
- **Code de Commerce**
  https://rnesm.justice.gov.ma/Documentation/MA/3_TradeRecord_fr-FR.pdf 
- **Code du Travail**
  https://miepeec.gov.ma/espace-travail/ministere-emploi-legislation-et-reglementations/?lang=fr
- **Code des Obligations et des Contrats**
  https://rnesm.justice.gov.ma/Documentation/MA/4_ONC_Law_fr-FR.pdf

These were prepared for the RAG by converting them into `.txt` files through a semi-manual process supported by `cleaning.py`.

A special thanks to **Ilyass Allouchi** for his help with data sourcing and model evaluation.

---

## 🚀 How to Run the Project

### Prerequisites
1. Ensure all dependencies are installed: `requirements.txt`.
2. Add a `CHANGE.json` file to `/app/data` containing your Google Cloud Translate API JSON key.
3. Add a `.env` file in the `/app` folder with your OPENAI_API_KEY.

Launch Instructions
Run the chatbot backend:
```bash
python -m uvicorn fastapi_app:app --reload
```

Run the chatbot frontend:
```bash
python -m streamlit run Accueil.py
```

# BY PASTA CORP. / TEAM 89 --> MoroccoAI Hackathon 2024
Taha El Hihi
Andreas Salice
Samy Sidki
Pascalis Felahidis
Ayman Zeriouh
