# **Team AI_TURTLEFORCE**  

## **PainSense: AI-Driven Pain Detection and Chatbot Assistance**
---
## **Abstract**

### **Background and Problem Statement**  
Accurate and timely pain detection is a persistent challenge in healthcare, particularly for individuals unable to communicate effectively. This project proposes an automated AI-driven solution to detect, analyze, and manage pain using multimodal inputs such as audio and video.

### **Impact and Proposed Solution**  
The PainSense system leverages computer vision, audio analysis, and natural language processing to:  
1. Detect pain-related signals from video and audio inputs.  
2. Provide real-time feedback through an AI-powered chatbot.  
3. Support healthcare providers and caregivers with actionable insights for improved decision-making.  

### **Outcomes and Deliverables**  
- **Multimodal Pain Detection**: Combines facial expression recognition (FER) and audio sentiment analysis.  
- **Interactive Chatbot**: Offers real-time assistance and pain-related advice.  
- **Visualization Tools**: Provides graphs to track pain levels over time.  
- **User-Friendly Interface**: Accessible via Flask API and Gradio interface.  

---

## **Key Features**
1. **Multimodal Analysis**: Integrates audio (via Wav2Vec2) and video (via FER) models for pain detection.  
2. **Customizable Thresholds**: Allows configuration of pain intensity and confidence thresholds.  
3. **Real-Time Feedback**: Provides immediate results and chatbot recommendations.  
4. **Data Visualization**: Displays pain trends through graphs for better insights.  

---

## **System Requirements**
- Python 3.8 or later  
- Required Libraries: Install via `requirements.txt`  

---

## **How to Run the Project**

1. **Clone the Repository**:  
   ```bash
   git clone <repository-url>
   cd PainSense
   ```
2. **Install Dependencies**:  
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the Flask Server**:  
   ```bash
   python app.py
   ```
4. **Launch Gradio Interface**:  
   Open the provided link in your terminal to access the interface in your browser.

---

## **Instructions**

### **Input Upload**  
1. Upload an **audio** (e.g., `.mp3`, `.wav`) or **video** (e.g., `.mp4`, `.avi`) file.  
2. Click **Submit** to analyze the input.

### **Results Display**  
- **Pain Detection Result**: Indicates whether pain is detected.  
- **Average Pain Score**: Summarizes overall pain intensity.  
- **Pain Trend Graph**: Visualizes pain levels over time.

### **Chatbot Interaction**  
- Interact with the chatbot by typing queries in the input box.  
- Receive personalized recommendations and contextual assistance.  

---

## **System Architecture**

### 1. **Pain Detection**  
- **Facial Expression Recognition (FER)**: Detects pain-related emotions (e.g., sadness, fear) from video frames.  
- **Audio Sentiment Analysis**: Identifies pain-related cues in voice recordings using Wav2Vec2.  

### 2. **Data Fusion**  
- Combines audio and video analysis results using a weighted average approach.

### 3. **Visualization**  
- Generates graphical representations of pain scores over time.  
- Allows users to configure thresholds for better analysis.

### 4. **Chatbot**  
- Powered by Groq API to deliver contextual responses.  
- Adapts recommendations based on pain detection results.  

---

## **Project Workflow**

1. **Main Entry Point**:  
   - The project begins at `index.php`, which redirects users to `hackathon.html`.  

2. **User Interface**:  
   - `hackathon.html` serves as the primary interface, integrating HTML, CSS, and JavaScript for navigation.  

3. **Authentication**:  
   - `process.php` handles sign-up and log-in functionalities, managing database interactions.  

4. **Chatbot**:  
   - After authentication, users access `chatbot.html` to interact with the chatbot and explore pain analysis results.  

---

## **Acknowledgements**
We thank the creators of these technologies:  
- [FER](https://github.com/justinshenk/fer) for facial emotion recognition.  
- [Wav2Vec2](https://huggingface.co/models) for audio sentiment analysis.  
- [Gradio](https://gradio.app/) for interactive interfaces.  
- [Flask](https://flask.palletsprojects.com/) for backend integration.  

---

## **Future Enhancements**
1. Add multilingual support for the chatbot.  
2. Enhance detection models for improved accuracy.  
3. Integrate wearable device compatibility for real-time monitoring.  
4. Expand capabilities to generate AI-driven radiology reports:  
   - Detailed reports for radiologists in English and French.  
   - Simplified summaries in Darija (Moroccan Arabic) for patients.  
5. Explore advanced multi-modal fusion techniques.  

--- 
