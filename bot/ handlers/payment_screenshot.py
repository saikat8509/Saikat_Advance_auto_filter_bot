import os
import re
import pytesseract
from PIL import Image
from io import BytesIO
from datetime import datetime
from pyrogram import Client, filters
from pyrogram.types import Message

from config import SCREENSHOT_AI_PROVIDER, PREMIUM_PLANS
from bot.utils.premium import add_premium_user
from bot.utils.database import get_user_referrer, increment_referral_points
from config import ADMIN_ID

# Optional: Configure Tesseract path if not in environment
pytesseract.pytesseract.tesseract_cmd = os.getenv("TESSERACT_PATH", "/usr/bin/tesseract")

# Regex to match amount like ₹49, ₹99 etc.
AMOUNT_PATTERN = re.compile(r"(?:₹|INR)\s?(\d{2,4})")

@Client.on_message(filters.private & filters.photo)
async def handle_payment_screenshot(client: Client, message: Message):
    if message.caption and "/verify" not in message.caption.lower():
        return

    user_id = message.from_user.id

    # Download the image
    file = await message.download(in_memory=True)
    img = Image.open(BytesIO(file.getvalue()))

    # OCR to extract text
    try:
        text = pytesseract.image_to_string(img)
    except Exception as e:
        await message.reply_text("❌ Failed to read screenshot. Try sending a clearer image.")
        return

    # Find payment amount
    match = AMOUNT_PATTERN.search(text)
    if not match:
        await message.reply_text("❌ Couldn't detect a valid payment amount in your screenshot.")
        return

    amount = int(match.group(1))

    # Match to a plan
    selected_plan = None
    for plan_id, plan in PREMIUM_PLANS.items():
        if int(plan["price"]) == amount:
            selected_plan = plan
            break

    if not selected_plan:
        await message.reply_text("❌ No premium plan matched the detected payment amount. Please contact admin.")
        await client.send_message(
            ADMIN_ID,
            f"❗ Unmatched payment screenshot from [{message.from_user.first_name}](tg://user?id={user_id}).\nDetected amount: ₹{amount}"
        )
        return

    # Add premium access
    await add_premium_user(user_id, selected_plan["days"])

    # Handle referral bonus
    ref_by = await get_user_referrer(user_id)
    if ref_by:
        await increment_referral_points(ref_by)

    await message.reply_text(
        f"✅ Payment verified successfully!\n\n🎉 Premium access granted for {selected_plan['days']} days.\n\nEnjoy ad-free fast downloads!"
    )

    # Notify admin
    await client.send_message(
        ADMIN_ID,
        f"✅ Verified payment screenshot from [{message.from_user.first_name}](tg://user?id={user_id}).\nPlan: {selected_plan['label']} (₹{amount})"
    )
