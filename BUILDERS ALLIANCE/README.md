# Terhal 🗺️⁀જ✈︎ 🇲🇦

<div align="center">
    <img src = "./Terhal_bot.png" alt = "terhal logo" width = "300px" height = "300px" >
</div>

##  Background and Problem Statement: 💢

Salma and Zineb are planning to visit 5 Moroccan cities during their 1-week vacation ⏳, but the real challenge is the planning process. They’ve learned that **for every week of travel**, they need **3 weeks of planing**, from **finding the best spots to visit to understanding transportation options** ˚˖𓍢ִ໋🍃˚.⛰️⋆☁️. Yet, they only speak **DARIJA**, which makes it hard for them to search in foreign languages. They tried **consulting a guide**, but it was **5 times more expensive than expected** and felt too **general**. This issue is holding them back 😟, and it’s affecting Morocco’s **tourism sector** 📉, which **contributes 7% of GDP**. 

Do we really need weeks of prep for just 1 week of travel? And do we need to speak foreign languages to travel in our own country ⁉️


##  Impact and Proposed Solution: 💡

Terhal is a chatbot 🤖 powered by LLMs (GPT-4 and Terjman), featuring an easy-to-use interface designed for Moroccan travelers passionate about using **DARIJA** while searching for the best places to visit in Morocco. It represents a brand-new way to help travelers find the best spots without investing too much time in preparation (time is money 💰). Not only that, it breaks down language barriers by incorporating the casual dialect **DARIJA** into the search. While built on existing solutions, Terhal combines the trio of **cost, quality, and time**, offering Moroccan travelers personalized recommendations in under 10 minutes, all in their mother tongue.

##  Project Outcomes and Deliverables: 🎯

- **Finding the best spots** to visit in each city in Morocco.
- **Time reduction** in planning, cutting trip preparation from 3 weeks to just 10 minutes.
- **Personalized recommendations** to find the best places for each traveler's needs.
- **Moroccan Dialect Support**, Terhal is tailored for Moroccan travelers and can understand and interact with over 90% accuracy in DARIJA.
- **Simple Interface**, The interaction with Terhal is through Terhal Bot, a beginner-friendly user interface with simple components to enhance accessibility for all users.

##  Instructions: 🛠️

The repository is organised following this layout:

```markdown

BUILDERS ALLIANCE/
├── code/
│   ├── ai_api_and_deployment/
│   │   ├── app/
│   │   ├── dataset/
│   │   ├── model/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── Dockerfile
│   │   ├── .env
│   │   └── requirements.txt
│   └── webApp/
│       ├── chat.html
│       ├── script.js
│       ├── styles.css
│       ├── requirements
│       └── package.json
|
├── presentation.pdf
├── demo
├── Terhal Logo
├── requirements.txt
├── .gitignore
└── README.md

```

### Prerequisites ⚙️

Before starting, ensure you have the following installed:
- **Python** (3.9 or later)
- **Node.js** (16.x or later) and **npm**
- **Docker** (optional, for containerized deployment)
- An internet connection to access the deployed AI API hosted on [Render](https://render.com) (free hosting).

---

### Installation and Setup

#### Clone the Repository

To begin, clone this repository to your local machine and navigate to the project folder:

```bash
git clone https://github.com/salmaelbarbori/2024-InnovAI-Hackathon/tree/main/BUILDERS%20ALLIANCE
cd 2024-InnovAI-Hackathon/BUILDERS%20ALLIANCE
```

#### Navigate to the **ai_api_and_deployment** folder:

```bash
cd builders/code/ai_api_and_deployment
```

Install the Python dependencies:

```bash
pip install -r requirements.txt
```

uvicorn main:app --reload

```bash
uvicorn main:app --reload
```

#### Run the Application 

Install Python dependencies from the main requirements.txt:

```bash
Install Python dependencies from the main requirements.txt:
```

Navigate to the webApp folder and install npm dependencies:

 ```bash
cd builders/code/webApp
npm install
```

Run the Application : 🔮

```bash
node proxy-server.js
 ```

 ## Pitch 🎤
 
[Terhal Pitch](https://drive.google.com/file/d/10b7Zw1034V-roZMKNyduOkKAPS2VeWRz/view?usp=sharing)

 ## Demo 🔮

[Terhal Bot](https://drive.google.com/file/d/1JIDRnFU8lKGONttrHCC4TfDb2P7j8hXG/view?usp=sharing)