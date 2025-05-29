import os
import re
import pytesseract
from PIL import Image
from io import BytesIO
from datetime import datetime
from pyrogram import Client, filters
from pyrogram.types import Message

from config import ENABLE_SCREENSHOT_AI, OCR_PROVIDER, PREMIUM_PLANS, ADMIN_ID
from bot.utils.premium import add_premium_user
from bot.utils.database import get_user_referrer, increment_referral_points

# Regex to extract amount like ₹99 or INR 49
AMOUNT_PATTERN = re.compile(r"(?:₹|INR)\s?(\d{2,4})")

@Client.on_message(filters.private & filters.photo)
async def handle_payment_screenshot(client: Client, message: Message):
    if not ENABLE_SCREENSHOT_AI or OCR_PROVIDER.lower() != "tesseract":
        return  # Feature disabled or unsupported provider

    if message.caption and "/verify" not in message.caption.lower():
        return

    user_id = message.from_user.id

    try:
        # Download and load image
        file = await message.download(in_memory=True)
        img = Image.open(BytesIO(file.getvalue()))

        # Extract text using Tesseract
        text = pytesseract.image_to_string(img)
    except Exception as e:
        await message.reply_text("❌ Couldn't process the screenshot. Please try sending a clearer image.")
        return

    # Search for a matching amount in the extracted text
    match = AMOUNT_PATTERN.search(text)
    if not match:
        await message.reply_text("❌ Couldn't detect a valid payment amount in your screenshot.")
        return

    amount = int(match.group(1))

    # Identify the matched premium plan
    matched_plan = None
    for plan_id, plan in PREMIUM_PLANS.items():
        if int(plan["price"]) == amount:
            matched_plan = plan
            break

    if not matched_plan:
        await message.reply_text("❌ Payment amount detected, but it doesn't match any available premium plan.")
        await client.send_message(
            ADMIN_ID,
            f"⚠️ Unmatched payment screenshot from [{message.from_user.first_name}](tg://user?id={user_id}).\n"
            f"Detected amount: ₹{amount}"
        )
        return

    # Grant premium access
    await add_premium_user(user_id, matched_plan["days"])

    # Reward referral if exists
    referrer_id = await get_user_referrer(user_id)
    if referrer_id:
        await increment_referral_points(referrer_id)

    await message.reply_text(
        f"✅ Payment verified successfully!\n\n🎉 You now have premium access for {matched_plan['days']} days!"
    )

    await client.send_message(
        ADMIN_ID,
        f"✅ Verified payment from [{message.from_user.first_name}](tg://user?id={user_id}).\n"
        f"Plan: {matched_plan['label']} (₹{amount})"
    )
