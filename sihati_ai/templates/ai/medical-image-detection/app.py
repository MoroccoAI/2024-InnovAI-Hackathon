import streamlit as st
import google.generativeai as genai
import base64
from api_key import api_key
from deep_translator import GoogleTranslator

# Configure genai with api_key
genai.configure(api_key=api_key)
 
# Create the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}
 
# Set safety settings
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"}
]
 
# Model configuration
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
)
 
system_prompt = """
As a highly skilled medical practitioner specializing in image analysis, you are tasked with examining medical images for a renowned hospital. You should provide diagnostic insights, possible treatment plans, and recommend medications based on the medical conditions identified in the images.
"""
 
# Set the page config
st.set_page_config(page_title="SIHATIAI Analytics", page_icon=":robot:")
 
# Set the title
st.title("صِحَتِي ❤️ | 📷 صورة | 📊 تحليلات")
st.subheader("تطبيق يمكنه مساعدة المستخدمين في تحديد الصور الطبية.")
 
# **Step 1: Medical Image Analysis**
uploaded_file = st.file_uploader("Upload the medical image for analysis", type=["png", "jpg", "jpeg"])
submit_button = st.button("توليد التحليل")
 
if submit_button and uploaded_file:
    # Encode the image
    image_data = uploaded_file.read()
    encoded_image = base64.b64encode(image_data).decode('utf-8')
   
    # Create the prompt parts
    prompt_parts = [
        {"text": system_prompt},
        {"mime_type": "image/jpeg", "data": encoded_image}
    ]
   
    try:
        with st.spinner('Analyzing the image and generating a response...'):
            response = model.generate_content(prompt_parts)
           
            if response.text and response.text.strip():
                cleaned_text = response.text.strip()
                translated_text = GoogleTranslator(source='en', target='ar').translate(cleaned_text)
               
                # Display the Arabic text properly formatted
                st.markdown(
                    f"""
                    <div style="direction: rtl; text-align: right; font-family: 'Arial', sans-serif; font-size: 18px;">
                        {translated_text}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.error("The generated response is empty. Please try again.")
    except Exception as e:
        st.error(f"Error during generation: {e}")
 
# **Step 2: Condition Description and Medication Recommendation**
condition_description = st.text_area("يرجى وصف حالتك الطبية أو الأعراض التي تشعر بها:")
 
medication_button = st.button("توصية بالأدوية")
 
medication_recommendations = None  # Variable to store medication recommendations
 
if medication_button and condition_description:
    # Create the prompt for generating medication recommendations
    condition_prompt = f"بناءً على الحالة التالية: {condition_description}، قدم قائمة بالأدوية أو العلاجات الموصى بها لهذه الحالة."
 
    try:
        with st.spinner('جاري توليد التوصيات بالأدوية...'):
            condition_response = model.generate_content([{"text": condition_prompt}])
 
            if condition_response.text and condition_response.text.strip():
                # Translate response to Arabic if the response is in another language
                translated_condition_response = GoogleTranslator(source='en', target='ar').translate(condition_response.text.strip())
               
                # Display the Arabic text properly formatted
                st.markdown(
                    f"""
                    <div style="direction: rtl; text-align: right; font-family: 'Arial', sans-serif; font-size: 18px;">
                        {translated_condition_response}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
               
                # Store the recommendations for download
                medication_recommendations = translated_condition_response
            else:
                st.error("لم يتم العثور على توصيات للأدوية لهذه الحالة.")
    except Exception as e:
        st.error(f"خطأ أثناء توليد التوصيات بالأدوية: {e}")
 
# **Step 3: Download Recommendations**
if medication_recommendations:
    # Convert the recommendations to a downloadable file (txt)
    def download_file(content, filename):
        b64 = base64.b64encode(content.encode()).decode()
        href = f'<a href="data:file/txt;base64,{b64}" download="{filename}">تحميل التوصيات</a>'
        return href
 
    st.markdown(download_file(medication_recommendations, "medication_recommendations.txt"), unsafe_allow_html=True)

# **Step 4: Doctor Recommendation Based on Illness Type**
illness_type = st.text_input("أدخل نوع المرض:", placeholder="مثل: السكري، أمراض القلب، الصداع النصفي")
 
recommend_doctor_button = st.button("توصية بنوع الطبيب")
 
if recommend_doctor_button and illness_type.strip():
    # Create a prompt for suggesting a doctor based on the entered illness type
    doctor_prompt = f"""
    بناءً على المرض المدخل: {illness_type}، ما هو نوع الطبيب المختص الذي يجب زيارته؟ قدم إجابة مختصرة ومباشرة.
    """
    try:
        with st.spinner('جاري تحليل نوع المرض وتوليد التوصية...'):
            doctor_response = model.generate_content([{"text": doctor_prompt}])
 
            if doctor_response.text and doctor_response.text.strip():
                # Translate the response to Arabic
                translated_doctor_response = GoogleTranslator(source='en', target='ar').translate(doctor_response.text.strip())
 
                # Display the recommendation properly formatted
                st.markdown(
                    f"""
                     <div style="direction: rtl; text-align: right; font-family: 'Arial', sans-serif; font-size: 18px;">
                      : يُوصى بزيارة     <span style="color: green; font-weight: bold;">{translated_doctor_response}</span>.
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.error("لم يتم العثور على توصية بطبيب مختص لهذه الحالة. يرجى المحاولة مرة أخرى.")
    except Exception as e:
        st.error(f"خطأ أثناء توليد التوصية بالطبيب: {e}")
else:
    if recommend_doctor_button:
        st.warning("يرجى إدخال نوع المرض للحصول على التوصية.")

# *Step 5 : localisation of hospital 
import requests
from opencage.geocoder import OpenCageGeocode
 
# Fonction pour obtenir les coordonnées à partir de l'adresse
def get_coordinates(address):
    key = 'df3ed943a9fa4ceb89124b74a86cd7cc'  # Remplacez par votre clé API OpenCage
    geocoder = OpenCageGeocode(key)
    result = geocoder.geocode(address)
   
    if result:
        return result[0]['geometry']['lat'], result[0]['geometry']['lng']
    else:
        return None, None
 
# Fonction pour effectuer une requête Overpass à partir des coordonnées
def search_places(latitude, longitude, place_types=["doctor", "hospital", "clinic"]):  # Recherche de plusieurs types
    place_types_query = " ".join([f'node["amenity"="{place_type}"](around:10000,{latitude},{longitude});'
                                  f'way["amenity"="{place_type}"](around:10000,{latitude},{longitude});'
                                  f'relation["amenity"="{place_type}"](around:10000,{latitude},{longitude});'
                                  for place_type in place_types])
   
    query = f"""
    [out:json];
    (
        {place_types_query}
    );
    out body;
    """
   
    overpass_url = "http://overpass-api.de/api/interpreter"
    response = requests.get(overpass_url, params={'data': query})
   
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Erreur Overpass: {response.status_code}")
        return None
 
# Interface utilisateur Streamlit
def main():
    st.title("Recherche de Lieux autour de l'Adresse")
   
    # Saisie de l'adresse
    address = st.text_input("Entrez l'adresse ou la ville", "Casablanca, Maroc")
   
    # Bouton de recherche
    if st.button("Rechercher les lieux"):
        if address:
            latitude, longitude = get_coordinates(address)
           
            if latitude and longitude:
                st.write(f"Événement trouvé à: {address}")
                st.write(f"Événements autour des coordonnées: Latitude {latitude}, Longitude {longitude}")
               
                # Recherche des lieux à proximité
                place_types = ["doctor", "hospital", "clinic"]  # Types modifiés pour inclure plusieurs services
                results = search_places(latitude, longitude, place_types)
               
                if results:
                    st.write(f"Trouvé {len(results['elements'])} lieux à proximité de {address}.")
                    for element in results['elements']:
                        name = element.get('tags', {}).get('name', 'Inconnu')
                        amenity_type = element.get('tags', {}).get('amenity', 'Inconnu')
                        lat = element.get('lat') or element.get('center', {}).get('lat', 'Inconnu')
                        lon = element.get('lon') or element.get('center', {}).get('lon', 'Inconnu')
                       
                        # Construction du lien vers Google Maps
                        google_maps_link = f"https://www.google.com/maps?q={lat},{lon}"
                       
                        st.write(f"Nom: {name}, Type: {amenity_type}, Lien Google Maps: [Voir sur Google Maps]({google_maps_link})")
                else:
                    st.write("Aucun lieu trouvé.")
            else:
                st.error("Impossible de récupérer les coordonnées pour cette adresse.")
        else:
            st.error("Veuillez entrer une adresse valide.")
 
if __name__ == "__main__":
    main()
