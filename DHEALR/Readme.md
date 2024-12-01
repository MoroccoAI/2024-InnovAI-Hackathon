# Medical Assistance and Medication Information App

## Abstract

### Background and Problem Statement

In Morocco, many people struggle to access healthcare or receive timely advice due to language barriers, lack of resources, or the unavailability of nearby medical professionals. Specifically, Moroccan users face challenges when trying to use large language models or medical applications for self-diagnosis and understanding their health conditions. Additionally, many patients fail to fully read or understand the information provided with medications, leading to potential misuse or missed side effects. Furthermore, patients often do not know whether a medical issue is urgent or not.

The lack of accessibility to reliable health resources in Moroccan Arabic (Darija) compounds the problem, as most available applications and medical information are in English or other languages that are not native to many Moroccans. This can prevent them from making informed decisions about their health, and hinder their ability to manage their conditions appropriately.

### TEAM MENBERS

Anas Ouhannou,
Belkhlifi Anas,
Imane El Maakoul,
Mayssae Jabbar,
Wajih Esghayri,

### Impact and Proposed Solution

This project aims to solve these problems by providing a web application that allows Moroccan users to interact with a chatbot for medical assistance and pre-diagnosis. The application supports both Darija (Moroccan Arabic) and English, making it more accessible to the local population.

The application enables users to:
- **Pre-diagnose health conditions** based on symptoms and medical history (available in English, with Darija support coming soon).
- **Get information about medications**, including potential side effects and usage instructions, by either uploading an image of the medication or entering its name.
- **Ensure confidentiality** by allowing users to input and modify their personal information (age, gender, symptoms, medical history) and delete any sensitive information before submission.

By offering accurate and reliable medical guidance in Darija and English, the app helps Moroccan users make informed decisions about their health, and reduces the risk of misunderstanding medication instructions.

### Project Outcomes and Deliverables

The expected outcomes and deliverables of this project include:

- A fully functional **Streamlit-based web application** that allows Moroccan users to interact with the chatbot in both Darija and English.
- **OCR functionality** to extract text from images and provide medical advice based on the extracted information.
- A **pre-diagnosis feature** that helps users assess whether their symptoms are urgent and get recommendations for next steps.
- A **medication information feature** where users can upload images or enter medication names to get basic and crucial information, including potential side effects.
- **User confidentiality protection** by allowing them to modify or delete their personal information.
- **Multi-language support**, starting with English and Darija, ensuring accessibility for a wider audience.

---

The app leverages several libraries for text extraction (pytesseract), translation (googletrans), and language processing (transformers), making it a versatile tool for medical support and language interaction.


## Requirements

Make sure you have the following Python libraries installed:

- `streamlit`
- `pytesseract`
- `Pillow`
- `requests`
- `transformers`
- `llama_cpp`
- `googletrans==4.0.0-rc1`
- `deep_translator`
- `base64`

To install the required libraries, you can use `pip`:

```bash
pip install streamlit pytesseract pillow requests transformers llama_cpp googletrans==4.0.0-rc1 deep-translator
```

# Prerequisites for llama_cpp
The llama_cpp library requires a C++ compiler and additional tools for building C++ extensions. Follow these steps based on your operating system:

## 1. C++ Compiler:
Windows: Install Visual Studio Build Tools to get the required C++ compiler.
macOS: Install Xcode Command Line Tools by running:
```bash
xcode-select --install
```
Linux: Install GCC using:
```bash
sudo apt-get install build-essential
```
## 2. CMake:
CMake is required for building the C++ extensions. You can install it using:

Windows: Download CMake from the CMake website.
macOS/Linux: Use a package manager:
```bash
Copier le code
# On macOS (using Homebrew)
brew install cmake
```

# On Linux
```bash
sudo apt install cmake
```
Once the C++ compiler and CMake are installed, you can install the Python dependencies.

# Setup Instructions
## Install Tesseract OCR:
You need to have Tesseract installed on your system for pytesseract to work.

For Windows: Download Tesseract OCR
For macOS: brew install tesseract
For Linux: sudo apt install tesseract-ocr

API Keys (if required):
Some features (like the googletrans or other API-based services) may require API keys. Follow the respective API documentation to obtain the keys and set them up.

## Usage
Launch the App: To start the Streamlit app, navigate to the directory where your script is located and run the following command:

```bash
streamlit run app.py
```
## Upload Image:

On the app's interface, upload an image containing text.
The app will use Tesseract OCR to extract the text from the image.

## Translate Extracted Text:

After extracting the text, the app will automatically display the translated text in your chosen language.
You can choose from various translation models depending on your needs.
View Results: The app will show the extracted text, the translated text, and provide options to translate into different languages.

## Code Explanation

pytesseract: This library is used to extract text from the uploaded image using OCR.
transformers: The library is used to load models for language processing tasks.
googletrans and deep-translator: Used for translating the extracted text to different languages.

## DEMO

**DEMO Se7ti AI**
[Watch Demo Video](https://drive.google.com/file/d/1Rg5h8K12_dsOR2m1HFU702dJItnafCir/view?usp=sharing)

**DEMO Predignose feater**
[Watch Demo Video](https://drive.google.com/file/d/1Blmiiq0dIzbagf3TQVj_7qsq_NTVefYr/view?usp=sharing)

## PITCH 

**PRESENTATION**
[PRESENTATION](https://drive.google.com/file/d/1LGUlmX-YZrmItvKH3-42xZnDxnMzUhp6/view?usp=sharing)


**PITCH VIDEO**
[PITCH VIDEO](https://drive.google.com/file/d/17wR80-6jE0LndP9L-qVOwZ_pwePDYtZN/view?usp=sharing)


## Important Note

<p style="color:red;">
⚠️ If you encounter any problems running the project, please contact us for further and detailed instructions.

</p>
📧 **Email**: [anasouhnou@gmail.com](mailto:anasouhnou@gmail.com)
