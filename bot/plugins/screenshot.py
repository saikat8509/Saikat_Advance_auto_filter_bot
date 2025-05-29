# bot/plugins/screenshot.py

import io
import logging
from pyrogram import Client, filters
from pyrogram.types import Message
from config import ENABLE_SCREENSHOT_AI, OCR_PROVIDER
from bot.utils.database import add_premium_user, get_premium_plans
from PIL import Image
import pytesseract

logger = logging.getLogger(__name__)

async def extract_text_from_image(image_bytes: bytes) -> str:
    """
    Extract text from an image bytes using OCR provider.
    Currently supports 'tesseract'.
    """
    if OCR_PROVIDER.lower() == "tesseract":
        image = Image.open(io.BytesIO(image_bytes))
        text = pytesseract.image_to_string(image)
        return text
    else:
        logger.warning(f"OCR provider '{OCR_PROVIDER}' not supported yet.")
        return ""

def parse_payment_details(text: str) -> dict:
    """
    Parse OCR text to find payment amount and transaction ID.
    This function must be customized based on payment screenshot format.
    Example simplistic parse: looks for lines containing 'Amount' and 'Txn ID'
    """
    details = {}
    lines = text.split("\n")
    for line in lines:
        line = line.strip()
        if "amount" in line.lower():
            # Extract numbers from line
            import re
            amounts = re.findall(r"\d+\.?\d*", line)
            if amounts:
                details["amount"] = float(amounts[0])
        if "txn" in line.lower() or "transaction" in line.lower() or "id" in line.lower():
            # Extract txn id (simplistic)
            parts = line.split(":")
            if len(parts) > 1:
                details["txn_id"] = parts[1].strip()
    return details

def match_plan_by_amount(amount: float, plans: dict) -> dict:
    """
    Match the extracted amount with a premium plan.
    plans dict format:
    { "plan_key": {"price": 99, "days": 30, "label": "30 Days"} }
    """
    for key, plan in plans.items():
        if abs(plan.get("price", 0) - amount) < 1.0:  # Allow slight float diff
            return plan
    return None

@Client.on_message(filters.private & filters.photo)
async def payment_screenshot_handler(client: Client, message: Message):
    if not ENABLE_SCREENSHOT_AI:
        return  # feature disabled
    
    user_id = message.from_user.id
    photo = message.photo

    # Download the photo into memory
    photo_bytes = await client.download_media(photo, in_memory=True)

    # Extract text using OCR
    text = await extract_text_from_image(photo_bytes)
    logger.info(f"OCR text extracted: {text}")

    if not text:
        await message.reply_text("⚠️ Could not read the screenshot properly. Please send a clear payment screenshot.")
        return

    # Parse payment details
    payment_info = parse_payment_details(text)
    if "amount" not in payment_info:
        await message.reply_text("⚠️ Could not find the payment amount in the screenshot. Please try again.")
        return

    plans = await get_premium_plans()
    matched_plan = match_plan_by_amount(payment_info["amount"], plans)

    if not matched_plan:
        await message.reply_text(
            "❌ Payment amount does not match any of our premium plans.\n"
            "Please check and send a valid payment screenshot."
        )
        return

    # Grant premium to user
    days = matched_plan.get("days", 0)
    success = await add_premium_user(user_id, days)
    if success:
        await message.reply_text(
            f"✅ Payment verified successfully! You have been granted premium access for {days} days.\n"
            f"Thank you for your support!"
        )
    else:
        await message.reply_text("⚠️ There was an error granting your premium access. Please contact support.")

