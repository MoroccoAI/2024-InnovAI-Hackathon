import time

import streamlit as st
from constants import THRESHOLD
from data_utils import update_data
from extractor import PpdExtractor
from pdf2image import convert_from_bytes

st.title("File Uploader")

# File upload widget
uploaded_file = st.file_uploader("Choose a file", type=["pdf"])

if uploaded_file:
    # Display file name
    st.write(f"Uploaded file: {uploaded_file.name}")

    assert uploaded_file.name.endswith('.pdf')
    price, water_consumption = PpdExtractor.extract(uploaded_file)

    # Display the results
    st.write("### Extraction Results:")
    st.write(f"- **Price (Total TTC):** {price} MAD")
    st.write(f"- **Water Consumption:** {water_consumption} m³")

    update_data(price, water_consumption, city_threshold=40)
    st.success("Data updated")

    if water_consumption > 5:
        st.warning(f"Water usage ({water_consumption} liters) exceeded the threshold "
                   f"({THRESHOLD} liters). Redirecting to talk to the chatbot.")
        time.sleep(3)
        st.switch_page("pages/bot.py")

    st.subheader("Your bill")
    pdf_images = convert_from_bytes(uploaded_file.read())
    st.image(pdf_images[1], caption="Page 2", use_container_width=True)
