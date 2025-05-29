# bot/handlers/payment_screenshot.py

from pyrogram import filters, Client
from pyrogram.types import Message
from config import ENABLE_SCREENSHOT_AI, OCR_PROVIDER, PREMIUM_PLANS
from bot.utils.ocr import extract_payment_details
from bot.utils.database import grant_premium
from datetime import datetime, timedelta
import re

@Client.on_message(filters.private & filters.photo)
async def handle_payment_screenshot(client: Client, message: Message):
    if not ENABLE_SCREENSHOT_AI or OCR_PROVIDER.lower() != "tesseract":
        # Feature is disabled in .env or unsupported OCR provider
        return

    try:
        # Download image
        file_path = await message.download()

        # Run OCR on image
        ocr_result = extract_payment_details(file_path)
        if not ocr_result:
            await message.reply_text("❌ Failed to read payment details from the screenshot.")
            return

        amount = ocr_result.get("amount")
        txn_id = ocr_result.get("transaction_id")
        payment_time = ocr_result.get("timestamp")

        # Match amount to a plan
        matched_plan = None
        for days, details in PREMIUM_PLANS.items():
            if int(details["price"]) == int(amount):
                matched_plan = (int(days), details["label"])
                break

        if not matched_plan:
            await message.reply_text("❌ Invalid payment amount. Please check our premium plans and try again.")
            return

        # Grant premium if valid
        duration_days, label = matched_plan
        expiry_date = datetime.utcnow() + timedelta(days=duration_days)
        await grant_premium(user_id=message.from_user.id, expiry=expiry_date)

        await message.reply_text(
            f"✅ Payment of ₹{amount} detected!\n\n🎉 You've been granted **{label} Premium** access until `{expiry_date.strftime('%Y-%m-%d')}`.\n\nThank you!"
        )

    except Exception as e:
        await message.reply_text("⚠️ An error occurred while processing your screenshot.")
        print(f"[Screenshot AI Error] {e}")
