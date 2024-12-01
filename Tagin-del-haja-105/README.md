Tari9i: AI-Powered Career Counseling Chatbot

Abstract

Background and Problem Statement
Choosing a career path can be an overwhelming experience, particularly for students and young professionals who may not have access to personalized guidance. Traditional career counseling services are often inaccessible, expensive, or time-consuming. Furthermore, many individuals lack awareness of modern technological tools that can help them make informed decisions about their future.

Impact and Proposed Solution
Tari9i is an AI-powered career counseling chatbot designed to provide accessible, reliable, and instant career guidance. Leveraging cutting-edge natural language processing (NLP) models from Hugging Face and LangChain, Tari9i offers tailored advice based on the user's interests, skills, and goals. The chatbot provides a scalable and cost-effective solution, making career counseling available to underserved communities.

Project Outcomes and Deliverables
- Career Guidance Chatbot: An interactive chatbot that delivers personalized advice for career development.
- API Integration: Tari9i integrates a Hugging Face text generation model via a free API key for natural and context-aware responses.
- Deployment: A fully functional chatbot accessible via a web or mobile interface for real-time interactions.
- Documentation: Comprehensive user and developer documentation, including this README file, to ensure ease of use and maintainability.

Instructions

Prerequisites
1. Python: Ensure you have Python 3.10.2 or later installed.
2. Libraries: Install the required Python libraries.
3. API Key: Obtain a free API key from Hugging Face for the text generation model.

Setup
1. Clone the repository:
    git clone https://github.com/yassernamez03/2024-InnovAI-Hackathon.git
    cd 2024-InnovAI-Hackathon

2. Install dependencies:
    pip install -r requirements.txt

3. Add your Hugging Face API key:
    Create a .env file in the project root directory and add the following:
    HUGGINGFACE_API_KEY=your_api_key_here

Running the Project
1. Start the chatbot server:
    python app.py

2. Access the chatbot interface:
   Open your browser and navigate to http://localhost:8000 to interact with Tari9i.

Testing the Chatbot
Run the test suite to ensure everything is working as expected:
pytest tests/

Contributing
Contributions are welcome! Please check the CONTRIBUTING.md file for guidelines on contributing to Tari9i.

License
This project is licensed under the MIT License. See the LICENSE file for details.
