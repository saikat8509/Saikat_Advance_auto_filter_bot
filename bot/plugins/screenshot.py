import os
from pyrogram import filters, Client
from pyrogram.types import Message
from config import ENABLE_SCREENSHOT_AI, OCR_PROVIDER, PREMIUM_REWARD_DAYS, OWNER_USERNAME
from bot.utils.database import add_premium_user, get_user_referrer
from bot.utils.screenshot_ai import extract_payment_info
from datetime import datetime, timedelta

@Client.on_message(filters.private & filters.photo & filters.caption & filters.caption_contains("payment"))
async def handle_payment_screenshot(client: Client, message: Message):
    if not ENABLE_SCREENSHOT_AI:
        await message.reply("🛑 Screenshot AI verification is currently disabled.")
        return

    # Acknowledge receipt
    await message.reply("🧠 Analyzing your screenshot... Please wait.")

    # Download the image
    file_path = await message.download()

    # Extract data using OCR
    extracted = extract_payment_info(file_path, provider=OCR_PROVIDER)
    if not extracted:
        await message.reply("❌ Failed to verify payment. Please ensure the screenshot is clear.")
        return

    user_id = message.from_user.id
    valid_plan = extracted.get("valid_plan")
    amount = extracted.get("amount")

    if valid_plan:
        # Grant premium
        plan_days = int(valid_plan)
        expiry = datetime.utcnow() + timedelta(days=plan_days)
        await add_premium_user(user_id, expiry)

        # Referral bonus check
        referrer_id = await get_user_referrer(user_id)
        if referrer_id and PREMIUM_REWARD_DAYS:
            reward_expiry = datetime.utcnow() + timedelta(days=PREMIUM_REWARD_DAYS)
            await add_premium_user(referrer_id, reward_expiry)

        await message.reply(f"✅ Payment verified successfully!
🎉 You have been granted premium access for {plan_days} days.")
    else:
        await message.reply(f"⚠️ Couldn't find a valid plan in your screenshot.
Please send the payment screenshot to @{OWNER_USERNAME.lstrip('@')} for manual verification.")

    # Cleanup
    if os.path.exists(file_path):
        os.remove(file_path)
