# Aabar

Aabar is a centralized web app designed to monitor and manage underground water resources. It simplifies the well drilling licensing process, ensures compliance with water regulations, and predicts water availability using advanced data analytics. The app aims to combat illegal drilling and promote sustainable water management. Its target market includes government agencies, agricultural businesses, environmental organizations, and research institutions focused on water conservation.

# Main features:
- Real-time monitoring of wells
- A LLaMa-based chatbot fine-tuned on Moroccan water laws using RAG
- A water depth predictor using Random Forest and Graph-based radius neighbors regression fact-checked by a hydro-geo engineer
- A licensor after predicting the depth at a certain point


**Tested on Ubuntu, python 3.12.4, please make sure that the libraries are well installed, make sure that scikit-learn version is 1.3.2, failing in that will cause the predictor to not work as expected, and make sure sure that the jwt library is pyjwt, using an older python causes the whole dahboard to not function and using incorrect libraries may cause issues, here is a preliminary list of requirements, any issue or incorrect results will be caused either by the API keys or/and incorrect libraries as happened in the demo in the predictor after API key reset:**

```txt
camel_tools==1.5.5
earthengine_api==1.1.2
ee==0.2
fastapi==0.115.5
gdown==5.2.0
geopy==2.4.1
nltk==3.8.2
numpy==1.24.4
pandas==2.0.3
pinecone==5.4.1
plotly==5.24.1
protobuf==5.29.0
pydantic==2.10.2
Requests==2.32.3
SQLAlchemy==2.0.30
streamlit==1.35.0
tqdm==4.66.2
```

# Initialization:
```
python3 api_setup.py
```
# How to run (landing page):

```
npm i
npm run dev
```
# How to run (streamlit dashboard):

```
uvicorn fastapi_server:app --reload
streamlit run main.py
```
