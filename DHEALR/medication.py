import streamlit as st
import requests
from deep_translator import GoogleTranslator


# Function to fetch drug details
def fetch_drug_details(drug_name):
    OPENFDA_API_URL = "https://api.fda.gov/drug/label.json"

    try:
        # Query the API with the medicine name
        response = requests.get(
            f"{OPENFDA_API_URL}?search=openfda.brand_name:{drug_name}&limit=1"
        )
        response_data = response.json()

        # Check if results are found
        if "results" not in response_data:
            return "Ma kaynsh lma3loumat 3la had dawah."

        # Extract details from the first result
        drug_info = response_data["results"][0]

        details = {}
        details["name"] = drug_info.get("openfda", {}).get("brand_name", ["N/A"])[0]
        details["purpose"] = drug_info.get("purpose", ["N/A"])[0]
        details["warnings"] = drug_info.get("warnings", ["N/A"])[0]
        details["side_effects"] = drug_info.get("adverse_reactions", ["N/A"])[0]
        details["dosage"] = drug_info.get("dosage_and_administration", ["N/A"])[0]

        return details

    except Exception as e:
        return f"Kan chi moshkil: {e}"


# Function to translate text to Arabic (and modify to Moroccan Darija)
def translate_to_darija(text):
    try:
        # Translate text to Arabic
        translated_text = GoogleTranslator(source="en", target="ar").translate(text)

        # Adjust certain words or phrases to be more Darija
        darija_translation = translated_text.replace("نوصي", "Kan9der")
        darija_translation = darija_translation.replace("من فضلك", "3afak")
        darija_translation = darija_translation.replace("لا تستخدم", "Matsta3mlsh")
        darija_translation = darija_translation.replace(
            "الآثار الجانبية", "l7wayej lli kayn fiha"
        )

        return darija_translation
    except Exception as e:
        return f"Kan chi moshkil fi ttarjama: {e}"


# Streamlit UI
st.set_page_config(page_title="Ma3loumat Dawah", layout="wide")

st.title("B7t 3la Ma3loumat Dawah")
st.write("Dir smiya dial dawah f t7t bach tl9a chi ma3loumat fi l3arbiya w darija.")

# Input for drug name
medicine_name = st.text_input("Smiya dial dawah:")

# Display drug details when the button is clicked
if medicine_name:
    # Fetch drug details in Darija
    drug_info = fetch_drug_details(medicine_name)

    if isinstance(drug_info, dict):
        # Translate each piece of information to Darija
        translated_name = translate_to_darija(drug_info["name"])
        translated_purpose = translate_to_darija(drug_info["purpose"])
        translated_warnings = translate_to_darija(drug_info["warnings"])
        translated_side_effects = translate_to_darija(drug_info["side_effects"])
        translated_dosage = translate_to_darija(drug_info["dosage"])

        # Display the details in separate sections
        st.subheader("Smiya dial dawah")
        st.markdown(
            f"<div style='background-color: #f4f4f9; padding: 15px; border-radius: 10px; font-size: 16px; color: #333;'>{translated_name}</div>",
            unsafe_allow_html=True,
        )

        st.subheader("Chno kaydir")
        st.markdown(
            f"<div style='background-color: #f4f4f9; padding: 15px; border-radius: 10px; font-size: 16px; color: #333;'>{translated_purpose}</div>",
            unsafe_allow_html=True,
        )

        st.subheader("L7wayej lli kayn fiha")
        st.markdown(
            f"<div style='background-color: #f4f4f9; padding: 15px; border-radius: 10px; font-size: 16px; color: #333;'>{translated_warnings}</div>",
            unsafe_allow_html=True,
        )

        st.subheader("L'athar janibiya")
        st.markdown(
            f"<div style='background-color: #f4f4f9; padding: 15px; border-radius: 10px; font-size: 16px; color: #333;'>{translated_side_effects}</div>",
            unsafe_allow_html=True,
        )

        st.subheader("L'جرعة w ki tdiriha")
        st.markdown(
            f"<div style='background-color: #f4f4f9; padding: 15px; border-radius: 10px; font-size: 16px; color: #333;'>{translated_dosage}</div>",
            unsafe_allow_html=True,
        )

    else:
        st.error(drug_info)

    # Add some footer styling
    st.markdown(
        """
        <style>
            .footer {
                font-size: 14px;
                color: #777;
                text-align: center;
                margin-top: 50px;
                padding: 10px;
            }
        </style>
        <div class="footer">
            <p>Hada l'app kaykhllik t3rf ma3loumat 3la dawah f darija w l3arbiya.</p>
        </div>
    """,
        unsafe_allow_html=True,
    )
