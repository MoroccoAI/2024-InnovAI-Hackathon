import streamlit as st # type: ignore
import sys
import os

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json
import base64
from PIL import Image
import pytesseract
import cv2
import numpy as np
import pandas as pd
# Import your existing RAG system
from rag3 import RAGSystem, ArabicTextHandler, DataSource

def load_image(image_file):
    """
    Load and preprocess an image for OCR
    """
    # Read the image
    img = cv2.imdecode(np.fromstring(image_file.read(), np.uint8), cv2.IMREAD_COLOR)
    
    # Preprocess image for better OCR
    def preprocess_image(image):
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply thresholding to preprocess the image
        gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        
        # Apply denoising
        gray = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)
        
        return gray

    # Preprocess the image
    processed_img = preprocess_image(img)
    
    return processed_img

def perform_ocr(image):
    """
    Perform Optical Character Recognition on the image
    """
    # Use Tesseract to do OCR on the image
    # Supports multiple languages including Arabic
    text = pytesseract.image_to_string(image, lang='ara')
    
    return text

class GlutenAssistantApp:
    def __init__(self):
        # Initialize the RAG system
        self.gluten_assistant = RAGSystem()
        
        # Load data from CSV files
        self.gluten_assistant.data_sources = {
            DataSource.RECIPE_DATABASE: pd.read_csv("./Data/moroccan_recipes.csv"),
            DataSource.PRODUCT_CATALOG: pd.read_csv("./Data/moroccan_products.csv"),
            DataSource.NUTRITIONAL_DATABASE: pd.read_csv("./Data/nutritional_ref.csv"),  # Add the path if exists
        }
        
        
        # Set up Streamlit page configuration
        st.set_page_config(
            page_title="Moroccan Gluten Assistant",
            page_icon="🥖",
            layout="wide"
        )
    
    def run(self):
        """
        Main Streamlit application
        """
        # Title and description
        st.title("🥖 Moroccan Gluten Assistant")
        st.markdown("""
        **تحديد محتوى الغلوتين في المنتجات والوصفات المغربية**
        Identify Gluten Content in Moroccan Products and Recipes
        """)
        
        # Sidebar for navigation
        menu = st.sidebar.selectbox(
            "اختر وضع البحث",
            ["البحث النصي", "مسح المنتج", "قاعدة البيانات"]
        )
        
        if menu == "البحث النصي":
            self.text_search_mode()
        elif menu == "مسح المنتج":
            self.product_scan_mode()
        else:
            self.database_view_mode()
    
    def text_search_mode(self):
        """
        Text-based search mode
        """
        st.subheader("البحث النصي")
        
        # Search input
        query = st.text_input("أدخل اسم المنتج أو المكون", placeholder="مثل: كسكس، سردين")
        
        if st.button("ابحث"):
            if query:
                # Perform retrieval
                results = self.gluten_assistant.retrieve_relevant_info(query)
                
                # Generate response
                response = self.gluten_assistant.generate_response(results)
                
                # Display results
                st.markdown("#### نتائج البحث:")
                st.markdown(response)
                
                # Optional: Display detailed results
                with st.expander("تفاصيل إضافية"):
                    for result in results:
                        st.write(f"**{result.item_name}**")
                        st.write(f"يحتوي على الغلوتين: {'نعم' if result.contains_gluten else 'لا'}")
                        if result.gluten_sources:
                            st.write("مصادر الغلوتين:")
                            st.write(", ".join(result.gluten_sources))
                        if result.alternative_suggestions:
                            st.write("بدائل مقترحة:")
                            st.write(", ".join(result.alternative_suggestions))
    
    def product_scan_mode(self):
        """
        Product scanning mode with OCR
        """
        st.subheader("مسح المنتج")
        
        # Image upload
        uploaded_file = st.file_uploader(
            "قم بتحميل صورة المنتج", 
            type=['png', 'jpg', 'jpeg', 'webp'],
            help="قم بتحميل صورة للمنتج للتعرف على محتوى الغلوتين"
        )
        
        if uploaded_file is not None:
            # Display the uploaded image
            st.image(uploaded_file, caption="الصورة المرفوعة", use_column_width=True)
            
            # Perform OCR
            processed_image = load_image(uploaded_file)
            ocr_text = perform_ocr(processed_image)
            
            st.subheader("النص المستخرج:")
            st.text_area("النص", value=ocr_text, height=200)
            
            # Analyze extracted text
            if st.button("تحليل النص"):
                if ocr_text.strip():
                    # Perform retrieval on OCR text
                    results = self.gluten_assistant.retrieve_relevant_info(ocr_text)
                    
                    # Generate response
                    response = self.gluten_assistant.generate_response(results)
                    
                    # Display results
                    st.markdown("#### نتائج التحليل:")
                    st.markdown(response)
                else:
                    st.warning("لم يتم التعرف على أي نص. يرجى التأكد من جودة الصورة.")
    
    def database_view_mode(self):
        """
        View and explore the database
        """
        st.subheader("قاعدة بيانات المنتجات")
        
        # Tabs for different data sources
        tab1, tab2, tab3 = st.tabs([
            "قاعدة بيانات الوصفات", 
            "كتالوج المنتجات", 
            "المراجع الغذائية"
        ])
        
        with tab1:
            st.dataframe(self.gluten_assistant.data_sources[DataSource.RECIPE_DATABASE])
        
        with tab2:
            st.dataframe(self.gluten_assistant.data_sources[DataSource.PRODUCT_CATALOG])
        
        with tab3:
            st.dataframe(self.gluten_assistant.data_sources[DataSource.NUTRITIONAL_DATABASE])

def main():
    app = GlutenAssistantApp()
    app.run()

if __name__ == "__main__":
    main()

# Required dependencies:
# pip install streamlit pytesseract opencv-python-headless Pillow
# For Arabic OCR, you'll need to install Tesseract-OCR with Arabic language support