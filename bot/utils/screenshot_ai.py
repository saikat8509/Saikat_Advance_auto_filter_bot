import os
import pytesseract
import tempfile
import re
from PIL import Image
from google.cloud import vision
from config import OCR_PROVIDER


def extract_text_tesseract(image_path: str) -> str:
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        return text
    except Exception as e:
        return f"Tesseract OCR error: {e}"


def extract_text_google(image_path: str) -> str:
    try:
        client = vision.ImageAnnotatorClient()
        with open(image_path, 'rb') as image_file:
            content = image_file.read()
        image = vision.Image(content=content)
        response = client.text_detection(image=image)
        texts = response.text_annotations
        return texts[0].description if texts else ""
    except Exception as e:
        return f"Google OCR error: {e}"


def extract_text_from_image(file_bytes: bytes) -> str:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
        tmp_file.write(file_bytes)
        tmp_file_path = tmp_file.name

    if OCR_PROVIDER.lower() == "tesseract":
        extracted_text = extract_text_tesseract(tmp_file_path)
    elif OCR_PROVIDER.lower() == "google":
        extracted_text = extract_text_google(tmp_file_path)
    else:
        extracted_text = "Invalid OCR provider configuration."

    os.unlink(tmp_file_path)
    return extracted_text


def extract_payment_info(text: str) -> dict:
    # Attempt to extract relevant data (Amount, Date, Transaction ID, UPI ID)
    data = {}
    amount_match = re.search(r'\b(?:INR|Rs\.?|₹)\s?(\d{1,5})\b', text, re.IGNORECASE)
    if amount_match:
        data['amount'] = int(amount_match.group(1))

    txn_id_match = re.search(r'Txn(?:\s?ID)?[:\-\s]*([A-Z0-9]{6,})', text, re.IGNORECASE)
    if txn_id_match:
        data['txn_id'] = txn_id_match.group(1)

    upi_match = re.search(r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z]+\b', text)
    if upi_match:
        data['upi_id'] = upi_match.group(0)

    return data
