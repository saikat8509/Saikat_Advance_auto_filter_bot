
import io
import re
import logging
import aiohttp
from google.cloud import vision
from google.cloud.vision_v1 import types
from PIL import Image
from bot.utils.log import get_logger
from bot.config import SCREENSHOT_AI_CONFIG

logger = get_logger(__name__)

# Initialize Google Vision client (assumes GOOGLE_APPLICATION_CREDENTIALS env var set)
try:
    client = vision.ImageAnnotatorClient()
except Exception as e:
    logger.error(f"Failed to initialize Google Vision client: {e}")
    client = None


async def fetch_image_bytes(url: str) -> bytes:
    """
    Download image bytes from a URL asynchronously.
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.read()
                else:
                    logger.warning(f"Failed to fetch image, status code: {response.status}")
    except Exception as e:
        logger.error(f"Error fetching image from {url}: {e}")
    return b""


def parse_payment_text(text: str):
    """
    Parse payment info from extracted OCR text.
    Expected to find:
     - amount (₹ or Rs.)
     - transaction ID or ref no.
     - date/time
    Returns dict with keys: amount, txn_id, datetime or None if invalid.
    """
    # Example regex patterns (can be customized)
    amount_pattern = r"(₹|Rs\.?)\s?(\d+[.,]?\d*)"
    txn_pattern = r"(Txn\s?ID|Transaction\s?ID|Ref\.?|Reference)\s*[:\-]?\s*([A-Za-z0-9]+)"
    datetime_pattern = r"(\d{1,2}[/-]\d{1,2}[/-]\d{2,4}[\sT]?\d{1,2}:\d{2}(?:[:\d{2}]*)?)"

    amount = None
    txn_id = None
    datetime = None

    # Search amount
    match = re.search(amount_pattern, text, re.IGNORECASE)
    if match:
        amount = match.group(2).replace(",", "")

    # Search txn id
    match = re.search(txn_pattern, text, re.IGNORECASE)
    if match:
        txn_id = match.group(2)

    # Search date/time
    match = re.search(datetime_pattern, text)
    if match:
        datetime = match.group(1)

    if amount:
        return {"amount": amount, "txn_id": txn_id, "datetime": datetime}
    return None


async def extract_text_from_image_bytes(image_bytes: bytes) -> str:
    """
    Use Google Vision OCR to extract text from image bytes.
    """
    if not client:
        logger.error("Google Vision client not initialized.")
        return ""

    try:
        image = types.Image(content=image_bytes)
        response = client.text_detection(image=image)
        if response.error.message:
            logger.error(f"OCR error: {response.error.message}")
            return ""

        return response.full_text_annotation.text
    except Exception as e:
        logger.error(f"Exception during OCR: {e}")
        return ""


async def analyze_payment_screenshot(image_url: str):
    """
    Full pipeline:
    - fetch image bytes
    - extract text via OCR
    - parse payment info
    """
    logger.info(f"Analyzing payment screenshot: {image_url}")

    image_bytes = await fetch_image_bytes(image_url)
    if not image_bytes:
        logger.warning("No image bytes fetched.")
        return None

    text = await extract_text_from_image_bytes(image_bytes)
    if not text:
        logger.warning("No text extracted from image.")
        return None

    payment_info = parse_payment_text(text)
    if not payment_info:
        logger.info("No valid payment info found in OCR text.")
        return None

    logger.debug(f"Extracted payment info: {payment_info}")
    return payment_info

