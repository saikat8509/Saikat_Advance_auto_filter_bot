# bot/handlers/payment_screenshot.py

from pyrogram import Client, filters
from pyrogram.types import Message
from config import ENABLE_SCREENSHOT_AI, OCR_PROVIDER, PREMIUM_PLANS, ADMIN
from bot.utils.premium import grant_premium_access
from bot.utils.ocr import extract_payment_data
from bot.utils.database import save_payment_log

@Client.on_message(filters.private & filters.photo)
async def handle_payment_screenshot(bot: Client, message: Message):
    if not ENABLE_SCREENSHOT_AI or OCR_PROVIDER.lower() != "tesseract":
        return  # AI-based screenshot verification is disabled

    user = message.from_user
    photo = message.photo

    # Download the screenshot locally
    path = await bot.download_media(photo.file_id)
    
    # Extract data from the image using OCR
    try:
        payment_data = extract_payment_data(path)
    except Exception as e:
        await message.reply_text("❌ Failed to process screenshot. Please try again or contact support.")
        return

    if not payment_data or not payment_data.get("amount"):
        await message.reply_text("❌ Couldn't extract valid payment details. Please ensure the screenshot is clear.")
        return

    amount = float(payment_data.get("amount", 0))
    matched_plan = None

    # Match extracted amount to any premium plan
    for days, plan in PREMIUM_PLANS.items():
        if float(plan["price"]) == amount:
            matched_plan = int(days)
            break

    if matched_plan:
        # Grant premium access and notify the user
        await grant_premium_access(user.id, matched_plan)
        await message.reply_text(
            f"✅ Payment of ₹{amount} detected!\n"
            f"You have been granted **{matched_plan} days** of premium access. Enjoy!"
        )
    else:
        await message.reply_text(
            f"⚠️ Payment of ₹{amount} was detected but doesn't match any known premium plan.\n"
            f"Please contact the admin [here](https://t.me/{ADMIN}) with your screenshot.",
            disable_web_page_preview=True
        )

    # Save payment log for reference
    await save_payment_log(user.id, amount, payment_data)
