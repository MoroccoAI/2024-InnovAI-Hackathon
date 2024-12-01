import re

import pytesseract
from PyPDF2 import PdfReader

pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'


class PpdExtractor:
    @staticmethod
    def extract(pdf_path, page_number=2):
        reader = PdfReader(pdf_path)

        assert page_number >= 1 or page_number <= len(reader.pages)

        extracted_text = reader.pages[page_number - 1].extract_text()
        price_match = re.search(r'Total TTC\s+(\d+,\d+)', extracted_text)
        price = None
        if price_match:
            # Replace the comma with a dot and convert to float
            price = float(price_match.group(1).replace(",", "."))

        water_consumption = re.findall(r'(\d+)\s+Tranche', extracted_text)
        if len(water_consumption) == 0:
            water_consumption = 0

        elif len(water_consumption) >= 2:
            # Take only the first which corresponds to water consumption, other is for electricity
            water_consumption = int(water_consumption[0])

        return price, water_consumption


class ImageExtractor:
    def __init__(self, image):
        self.width, self.height = image.size
        self.image = image

    def extract_water_usage(self, text):
        # Extract water usage
        try:
            water_usage = re.findall(r"\d{2}/\d{2}/\d{4}\s+(\d+)", text.split("N°")[1])[-1]
            water_usage = int(water_usage)
        except Exception:
            water_usage = None

        return water_usage

    def extract_price(self, text):
        # Number that comes after "Sous total TTC"
        price = re.search(r"Sous total TTC[:\s]+([\d,]+(?:\.\d{1,2})?)", text)
        try:
            price = price.group(1)
            price = float(price.replace(",", "."))
        except Exception:
            price = None

        return price

    def extract(self):
        text = pytesseract.image_to_string(self.image)
        price = self.extract_price(text)
        water_usage = self.extract_water_usage(text)

        return price, water_usage
