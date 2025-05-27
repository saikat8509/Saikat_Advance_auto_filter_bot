from pyrogram import filters, Client
from pyrogram.types import Message
from config import OWNER_ID, PREMIUM_PLANS, ENABLE_SCREENSHOT_AI
from bot.utils.screenshot_ai import extract_payment_details
from bot.utils.database import add_premium_user
from datetime import datetime, timedelta
import logging

# Enable logging
logger = logging.getLogger(__name__)

@Client.on_message(filters.private & filters.photo)
async def handle_payment_screenshot(client: Client, message: Message):
    if not ENABLE_SCREENSHOT_AI:
        return

    user_id = message.from_user.id
    
    # Download the image
    photo = await message.download()
    
    # Extract payment data using OCR
    try:
        details = await extract_payment_details(photo)
    except Exception as e:
        logger.error(f"OCR failed: {e}")
        await message.reply("❌ Failed to read the screenshot. Please try again or contact admin.")
        return

    amount = details.get("amount")
    txn_id = details.get("txn_id")
    timestamp = details.get("timestamp")

    # Check against available plans
    matched = None
    for plan in PREMIUM_PLANS:
        if str(plan['price']) == str(amount):
            matched = plan
            break

    if matched:
        days = matched['days']
        expiry_date = datetime.utcnow() + timedelta(days=days)

        # Grant premium access
        await add_premium_user(user_id, expiry_date)
        await message.reply(
            f"✅ Payment of ₹{amount} verified!
"
            f"🎁 You've been granted **{days}-day Premium Access**.\n"
            f"🗓️ Expires on: {expiry_date.strftime('%Y-%m-%d %H:%M:%S')} UTC"
        )

        # Optional: log to admin
        await client.send_message(
            OWNER_ID,
            f"💰 Payment verified for user `{user_id}`\n"
            f"Amount: ₹{amount}\nTxn ID: {txn_id}\nTime: {timestamp}"
        )
    else:
        await message.reply(
            "⚠️ Couldn't auto-match this payment with any premium plan.\n"
            "Please wait while an admin manually verifies your payment."
        )

        # Forward screenshot and extracted info to admin
        await client.send_photo(
            OWNER_ID,
            photo=message.photo.file_id,
            caption=(
                f"⚠️ Manual verification needed for user `{user_id}`\n"
                f"Extracted Data:\nAmount: ₹{amount}\nTxn ID: {txn_id}\nTime: {timestamp}"
            )
        )
