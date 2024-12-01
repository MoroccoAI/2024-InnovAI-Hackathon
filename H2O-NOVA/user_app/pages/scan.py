import io

import streamlit as st
from data_utils import update_data
from extractor import ImageExtractor
from PIL import Image

st.set_page_config(page_title="Scan your water bill", page_icon="📸", layout="wide")

st.title("Scan your water bill")

captured_image = st.camera_input("Please capture only the part related to water")

if captured_image is not None:
    image = Image.open(io.BytesIO(captured_image.getvalue()))
    # image = Image.open("water_bill_maroc.jpg")
    st.image(image, use_container_width=True)

    # OCR
    with st.spinner("Extracting text..."):
        extractor = ImageExtractor(image)
        price, water_usage = extractor.extract()
        if price is None or water_usage is None:
            st.warning(
                """
                ### ⚠️ Alert
                Could not extract price or water usage. Please retake the photo.
                """
            )
            st.stop()

        update_data(price, water_usage, city_threshold=30)

    st.success("Data updated")
