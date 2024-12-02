# Hackathon


- Demo Link of the Marhaba-Morocco app [Marhaba-Morocco-app](https://marhaba-morocco.streamlit.app/)
- Figma design of the Marhaba-Morocco [Marhaba-Morocco-design](https://www.figma.com/design/e2Th6xQ4EvAaYwoPeHBzeN/Marhaba-Morocco?node-id=154-15406&t=giX5iXYplDUsToEY-1)
- Watch the video presentation of the Marhaba-Morocco app [video-presentation](https://drive.google.com/file/d/1eGzoz7EJ2z6cKwwEHQv68WUKnWRmE1mN/view?usp=sharing).
- Watch the video demo of the Marhaba-Morocco app [video-demo](https://drive.google.com/file/d/1P2S0oJvJQAcTiU3ctTCJRs2uIA5ngP43/view?usp=sharing).



## Abstract

### Background and Problem Statement

In today's fast-paced world, travelers often face challenges in finding reliable information about accommodations, local laws, cultural insights, and trip planning in Morocco. This project aims to streamline the process of gathering and providing this information, making it easier for users to plan their trips effectively.

### Impact and Proposed Solution

The proposed solution is a virtual concierge application that leverages AI to assist users in obtaining tailored recommendations for hotels, cultural insights, and legal information. By integrating various APIs and utilizing natural language processing, the application can provide accurate and relevant responses to user queries, enhancing the travel experience and ensuring users have access to the information they need.

### Project Outcomes and Deliverables

- A fully functional virtual concierge application that can:
  - Provide hotel recommendations based on user preferences.
  - Answer questions related to Moroccan culture and traditions.
  - Offer insights into local laws and regulations.
- Clear documentation on how to use the application.
- A user-friendly interface built with Streamlit for easy interaction.

## Instructions

1. **Clone the Repository**

   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Set Up Environment**

   - Ensure you have Python 3.8 or higher installed.
   - Create a virtual environment:
     ```bash
     python -m venv venv
     source venv/bin/activate  # On Windows use `venv\Scripts\activate`
     ```

3. **Install Dependencies**

   - Install the required libraries:
     ```bash
     pip install -r requirements.txt
     ```

4. **Set Up Environment Variables**

   - Create a `.env` file in the root directory and add your API keys:
     ```
     OPENAI_API_KEY=<your_openai_api_key>
     PINECONE_API_KEY=<your_pinecone_api_key>
     HOTELS_API_KEY=<your_hotels_api_key>
     ```

5. **Run the Application**

   - Start the Streamlit application:
     ```bash
     streamlit run main.py
     ```

6. **Interact with the Application**
   - Open your web browser and go to `http://localhost:8501` to start using the virtual concierge.

## Video Demo

- Watch the video demo of the Marhaba-Morocco app [here](https://drive.google.com/file/d/1P2S0oJvJQAcTiU3ctTCJRs2uIA5ngP43/view?usp=sharing).
