# Sahara Sage: “The Moroccan Digital Travel Companion” 🗺️✈️
![My Logo](https://github.com/Bocchi-K016/2024-InnovAI-Hackathon/raw/patch-1/QuBit/logo.png)
## Problem Statement: 🤔
Imagine planning your first vacation to Morocco 🏖️. You're excited to explore its bustling markets, beautiful landscapes, and rich culture, but you’re overwhelmed by the sheer amount of information out there. Searching for recommendations online takes hours, but most sources are either too general or not in your preferred language 🌍💬.

Hiring a local guide sounds appealing, but it’s too expensive 💸, and you don’t know if it's really necessary for a smooth trip. You simply want a stress-free, affordable way to navigate Morocco’s top attractions, transport options, and hidden gems.

Is there a way to simplify travel planning and access accurate, real-time information without breaking the bank? 
Can we make it easier for travelers to get tailored recommendations without language barriers? 🌐
How can technology like GenAI improve the tourism experience in Morocco and make it more accessible to everyone? 

## Proposed Solution: 💡
Sahara Sage is the perfect solution for modern travelers looking for an easy, affordable, and personalized way to explore Morocco 🏞️. By offering real-time, multilingual recommendations, this AI-powered chatbot eliminates the need for costly guides 💸, while making crucial information easily accessible. Whether it’s finding top attractions, navigating transportation, or discovering hidden gems, Sahara Sage ensures tourists have a smooth, stress-free experience 🌍💬, helping them make the most of their trip without language barriers or hours of research.

## Instructions: 🛠️
Here is an overview of the project folder layout and a description of each file:

```markdown
QuBit/
├── prepare_dataset.ipynb //a file where I combined 3 different datasets related to tourism in Morocco to create the main balanced json dataset 
├── deduplicated_dataset.json // the final version of the dataset
├── llama-2-7b-chat.ggmlv3.q8_0.bin //the open source LLM model used 
├── vectordb_create.py //the script used to create the embeddings and store them in FAISS victordb (it creates the vectorstore once executed)
├── requirements.txt //contains all the requirements that must be installed in the project environment 
├── model.py
├── chainlit.md
├── Public
    └── style.css
└── chainlit.yaml
```
### Prerequisites: ⚙️
To run the Sahara Sage chatbot, you will need the following:

- Python (preferably version 3.7+): Essential for running the code and managing dependencies.
- Git Bash: For version control and managing the repository.
- Anaconda: A Python distribution that helps manage environments and dependencies efficiently.
- Internet Connection: Required to download necessary libraries, models, and datasets.

### Installation and Setup: ⚙️
- To begin, clone this repository to your local machine and navigate to the project folder.
- Open the git bash in the project repository.
- Update and install conda packages:
```
conda init bash
conda install openssl
conda update conda
```
- Create and activate the conda environment required for the project:
```
conda create -n mychatbot python=3.10 -y
conda activate mychatbot
```
- Install all the required packages in mychatbot environment:
```
pip install -r requirements.txt
```
- Install the open source llm model in the main repository:
https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML/blob/main/llama-2-7b-chat.ggmlv3.q8_0.bin
- Run the vectordb_create.py to create the victorstore:
```
python vectordb_create.py
```
- Run the Model.py:
```
chainlit run model.py -w
```
##  Demo 🔮:
View the demo here: https://www.loom.com/share/f808b3c506c14a70837b94052b795ff8?sid=18c8dad9-9a19-44a9-8165-79117b1b74bd

If you have any questions or contributions don't hesitate. <3
