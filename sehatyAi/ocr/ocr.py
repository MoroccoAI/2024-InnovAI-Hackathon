import streamlit as st
import numpy as np
import cv2
import pytesseract
from PIL import Image
import tempfile
import os
import uuid
import fitz
from azure.storage.blob import BlobServiceClient
import subprocess
import threading
# import openai  # Import OpenAI SDK
import ollama

# Configuration and Credentials
CONNECTION_STRING = "BlobEndpoint=https://jhjfsdb.blob.core.windows.net/;QueueEndpoint=https://jhjfsdb.queue.core.windows.net/;FileEndpoint=https://jhjfsdb.file.core.windows.net/;TableEndpoint=https://jhjfsdb.table.core.windows.net/;SharedAccessSignature=sv=2022-11-02&ss=bfqt&srt=sco&sp=rwdlacupiytfx&se=2024-11-30T07:56:49Z&st=2024-11-29T23:56:49Z&spr=https,http&sig=6l9g7%2BATRsEjE3WuomwYYxBw3zyplw2W%2ByOtZ9HRWaM%3D"
CONTAINER_NAME = "store"
# OPENAI_API_KEY = "your-openai-api-key"  # Your OpenAI API key
# openai.api_key = OPENAI_API_KEY

class ImageProcessor:
    @staticmethod
    def preprocess_image(image_path):
        """Preprocess image for better OCR accuracy."""
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, processed = cv2.threshold(gray, 130, 255, cv2.THRESH_BINARY)
        return processed

    @staticmethod
    def extract_text(image_path):
        """Extract text from preprocessed image using Tesseract."""
        image = ImageProcessor.preprocess_image(image_path)
        text = pytesseract.image_to_string(image, lang="ara+eng+fra")
        return text

    @staticmethod
    def extract_images_from_pdf(pdf_path):
        """Extract images from PDF."""
        doc = fitz.open(pdf_path)
        images = []
        for page_number in range(len(doc)):
            pix = doc[page_number].get_pixmap(dpi=300)
            image_array = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
            if image_array.shape[2] == 4:
                image_array = cv2.cvtColor(image_array, cv2.COLOR_RGBA2RGB)
            images.append(image_array)
        return images

class AzureStorageManager:
    def _init_(self, connection_string, container_name):
        """Initialize Azure Blob Storage client."""
        self.blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        self.container_client = self.blob_service_client.get_container_client(container_name)

    def upload_file(self, file_path):
        """Upload file to Azure Blob Storage."""
        try:
            blob_client = self.container_client.get_blob_client(os.path.basename(file_path))
            with open(file_path, "rb") as data:
                blob_client.upload_blob(data, overwrite=True)
            return True
        except Exception as e:
            st.error(f"Azure Upload Error: {e}")
            return False

# class OpenAITextCorrector:
#     @staticmethod
#     def correct_text(ocr_text):
#         """Use OpenAI API to correct and structure OCR text."""
#         prompt = f"""
#         You are a professional medical prescription assistant.
#         Extract and structure medical prescription information precisely from the following text:

#         {ocr_text}

#         Provide a clean, structured output with:
#         - Doctor's Name
#         - Patient Name
#         - Date of Prescription
#         - Medicines:
#           * Name
#           * Dosage
#           * Instructions
#         """
#         try:
#             response = openai.Completion.create(
#                 model="gpt-4",  # You can also use "text-davinci-003" for cheaper options
#                 prompt=prompt,
#                 max_tokens=1000,
#                 temperature=0.5
#             )
#             corrected_text = response.choices[0].text.strip()
#             return corrected_text
#         except Exception as e:
#             st.error(f"OpenAI API Error: {e}")
#             return ""

class LLaMaTextCorrector:
    @staticmethod
    def correct_text(ocr_text):
        """Use LLaMa to correct and structure OCR text."""
        chat_history = [
            {"role": "system", "content": """You are a professional medical prescription assistant.
            You should always answer the question, no matter the quality of the input text.
            Make sure to structure your answer clearly and provide all the requested details !
            Don't give answers like : I can't help with that. Is there anything else I can help you with?"""},
            {"role": "user", "content": f"""
            You should Answer No Matter what ! Even if it is not well !
            Please analyze the following text carefully and provide the following details in a structured format:

            - Doctor's Name
            - Patient's Name
            - Date of Prescription
            - Medicines:
            * Name
            * Dosage
            * Instructions

            Here is the text to analyze:
            {ocr_text}
            """}
        ]

        try:
            answer = ollama.chat(model="llama3.2", messages=chat_history, stream=True)

            corrected_text = ""
            for token_dict in answer:
                token = token_dict["message"]["content"]
                corrected_text += token

            return corrected_text
        except Exception as e:
            st.error(f"LLaMa Error: {e}")
            return ""

def main():
    # Streamlit UI Configuration
    st.set_page_config(page_title="Se7ty Healthcare App", page_icon="🩺")
    st.image("images.jpg", width=150, caption="Se7ty Healthcare App", use_column_width=False)
    st.markdown("<h1>Se7ty Healthcare App</h1>", unsafe_allow_html=True)
    st.markdown("<p>Easily process and save your ordonnance (prescription).</p>", unsafe_allow_html=True)

    # File Upload
    uploaded_file = st.file_uploader("Upload an Image or PDF", type=["jpg", "jpeg", "png", "pdf"])
    use_camera = st.checkbox("Take a Photo with Your Camera")
    image_to_process = None

    if uploaded_file:
        file_type = uploaded_file.type
        if file_type == "application/pdf":
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
                temp_pdf.write(uploaded_file.read())
                pdf_images = ImageProcessor.extract_images_from_pdf(temp_pdf.name)
            if pdf_images:
                image_to_process = pdf_images[0]
                st.image(image_to_process, caption="First Page of Uploaded PDF", use_column_width=True)
        else:
            image_to_process = np.array(Image.open(uploaded_file))
            st.image(image_to_process, caption="Uploaded Ordonnance", use_column_width=True)

    elif use_camera:
        picture = st.camera_input("Capture your Ordonnance")
        if picture:
            image_to_process = np.array(Image.open(picture))
            st.image(image_to_process, caption="Captured Ordonnance", use_column_width=True)

    if image_to_process is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp:
            temp_image_path = temp.name
            cv2.imwrite(temp_image_path, cv2.cvtColor(image_to_process, cv2.COLOR_RGB2BGR))

        preprocessed_image = ImageProcessor.preprocess_image(temp_image_path)
        st.image(preprocessed_image, caption="Preprocessed Ordonnance", channels="GRAY")

        # Text Extraction
        recognized_text = ImageProcessor.extract_text(temp_image_path)
        st.text_area("Extracted Ordonnance Text", recognized_text, height=200)

        # Correct Text using OpenAI
        # corrected_text = OpenAITextCorrector.correct_text(recognized_text)
        corrected_text = LLaMaTextCorrector.correct_text(recognized_text)
        st.text_area("Structured Prescription Details", corrected_text, height=300)

        # Save Corrected Text
        random_file_name = f"data/corrected_ordonnance_{uuid.uuid4().hex}.txt"
        with open(random_file_name, "w", encoding="utf-8") as file:
            file.write(corrected_text)

        # Azure Storage Upload
        azure_manager = AzureStorageManager(CONNECTION_STRING, CONTAINER_NAME)
        if azure_manager.upload_file(random_file_name):
            st.success(f"Prescription details saved and uploaded to Azure: {random_file_name}")

        # Clean up temporary files
        os.remove(temp_image_path)
        os.remove(random_file_name)

if __name__ == "__main__":
    main()
