import os
import tempfile
import pytesseract
from PIL import Image
from datetime import datetime

from pyrogram import Client, filters
from pyrogram.types import Message

from config import PREMIUM_PLANS, AI_VERIFICATION_PROVIDER, MINIMUM_PAYMENT_AMOUNT
from bot.utils.database import add_premium_user
from bot.utils.time import get_plan_expiry
from bot.utils.logger import log

# AI Screenshot Verification
async def extract_text_from_image(image_path: str) -> str:
    if AI_VERIFICATION_PROVIDER == "tesseract":
        return pytesseract.image_to_string(Image.open(image_path))
    else:
        raise NotImplementedError("Only tesseract provider is supported currently.")

def extract_payment_info(ocr_text: str) -> dict:
    lines = ocr_text.splitlines()
    info = {
        "amount": None,
        "txn_id": None,
        "timestamp": None
    }
    for line in lines:
        if not info["amount"] and ("rs" in line.lower() or ₹ in line):
            for word in line.split():
                if word.replace(",", "").replace(".", "").isdigit():
                    try:
                        amt = float(word.replace(",", ""))
                        if amt >= MINIMUM_PAYMENT_AMOUNT:
                            info["amount"] = amt
                            break
                    except:
                        continue

        if not info["txn_id"] and ("txn" in line.lower() or "transaction" in line.lower()):
            words = line.split()
            for word in words:
                if len(word) >= 8 and any(char.isdigit() for char in word):
                    info["txn_id"] = word
                    break

        if not info["timestamp"] and any(tok in line.lower() for tok in ["am", "pm"]):
            info["timestamp"] = line.strip()

    return info

def get_matching_plan(amount: float) -> tuple:
    for days, plan in PREMIUM_PLANS.items():
        if amount >= plan["price"]:
            return days, plan["label"]
    return None, None

@Client.on_message(filters.private & filters.photo)
async def handle_payment_screenshot(client: Client, message: Message):
    user_id = message.from_user.id
    photo = message.photo

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tf:
            path = await message.download(file_name=tf.name)

        ocr_text = await extract_text_from_image(path)
        extracted_info = extract_payment_info(ocr_text)

        log(f"OCR extracted from user {user_id}: {extracted_info}")

        amount = extracted_info.get("amount")
        txn_id = extracted_info.get("txn_id")
        timestamp = extracted_info.get("timestamp")

        if not amount or not txn_id:
            await message.reply_text("❌ Could not verify the payment. Please make sure the screenshot is clear and try again or contact admin.")
            return

        plan_days, plan_label = get_matching_plan(amount)
        if not plan_days:
            await message.reply_text("❌ Payment amount does not match any valid premium plan.")
            return

        await add_premium_user(user_id, plan_days, plan_label)

        expiry_date = get_plan_expiry(plan_days)
        await message.reply_text(
            f"✅ Payment verified successfully!

💠 Premium Plan: {plan_label}
💰 Amount: ₹{amount}
📅 Expires on: {expiry_date.strftime('%d %B, %Y')}\n\nThank you for your support!"
        )

    except Exception as e:
        log(f"Error verifying screenshot: {e}")
        await message.reply_text("❌ An error occurred during verification. Please contact support.")
    finally:
        if os.path.exists(path):
            os.remove(path)
