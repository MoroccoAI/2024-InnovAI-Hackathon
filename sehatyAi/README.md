# SehatyAi: AI-Powered Personal Health Management App

- Watch the video demo of our app [video-demo](https://shorturl.at/HHoY6).

## Background and Problem Statement

In today's complex healthcare landscape, individuals and families face significant challenges in managing medical information, tracking health histories, and navigating healthcare services. Patients often struggle with:

- Fragmented medical record keeping
- Difficulty identifying appropriate medical specialists
- Limited insight into hereditary health risks
- Inefficient method of tracking family health histories
- Language barriers in healthcare communication

## Impact and Proposed Solution

SehatyAi introduces an innovative mobile application that transforms personal health management through intelligent AI-powered technology. By leveraging advanced document scanning, multilingual AI assistance, and comprehensive health tracking, the app provides:

- Centralized, secure medical document storage
- Intelligent health information extraction
- Personalized medical guidance
- Seamless doctor recommendation and navigation
- Comprehensive family health profile management

## Project Outcomes and Deliverables

The SehatyAi app will deliver:

- A user-friendly mobile application with intuitive health management features
- AI-driven medical document scanning and information extraction
- Multilingual (Arabic/English) health assistance
- Intelligent medical specialist recommendation system
- Secure, comprehensive family health profile tracking
- Map-integrated healthcare provider navigation

## Technology Stack

- **Frontend**: 
  - Streamlit - Main web interface
  - Chainlit - Chat interface
- **Backend**:
  - Python 3.9+
  - LangChain - For AI/LLM orchestration
  - ChromaDB - Vector database for document storage
  - Ollama - Local LLM integration
  - OpenCV - Image processing
  - PyPDF & PDFPlumber - PDF processing
  - Unstructured - Document parsing
  - ElevenLabs - Text-to-speech capabilities

## Prerequisites

Before running the application, ensure you have:

1. Python 3.9 or higher installed
2. Git installed
3. Ollama installed (for local LLM support)
4. Sufficient disk space for dependencies and document storage
5. A modern web browser

## Installation and Setup

1. Clone the repository:
   ```bash
   git clone [repository-url]
   cd sehatyAi
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirement.txt
   ```

4. Install and start Ollama (if not already done):
   ```bash
   # Follow Ollama installation instructions at: https://ollama.ai/
   # Pull the required model:
   ollama pull mistral
   ```

5. Set up the application:
   ```bash
   # Create necessary directories if they don't exist
   mkdir -p chroma_db
   mkdir -p data
   ```

## Running the Application

You can run the application in two different modes:

1. Streamlit Interface:
   ```bash
   streamlit run app_streamlit.py
   ```

2. Chainlit Chat Interface:
   ```bash
   chainlit run app_chainlit.py
   ```

The application will be accessible through your web browser at the provided local URL.
