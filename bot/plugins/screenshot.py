# bot/plugins/screenshot.py

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import ADMIN_ID, PAYMENT_PROOF_CHANNEL, TUTORIAL_CHANNEL
from utils.texts import screenshot_received_text

# Optional: Future OCR logic placeholder
# from utils.ocr import extract_payment_info, validate_payment

# /screenshot or "Send Payment Screenshot" button
@Client.on_message(filters.private & (filters.command("screenshot") | filters.photo))
async def receive_payment_screenshot(client: Client, message: Message):
    user = message.from_user

    # Ensure it's a photo (payment screenshot)
    if not message.photo:
        await message.reply_text("❌ Please send a valid payment *screenshot* as an image.", quote=True)
        return

    caption = f"🧾 *Payment Screenshot Received!*\n\n👤 User: `{user.first_name}` [`{user.id}`]\n"
    caption += f"🆔 Username: @{user.username or 'N/A'}"

    # Forward to admin or proof channel
    await message.forward(ADMIN_ID)
    if PAYMENT_PROOF_CHANNEL:
        await message.copy(PAYMENT_PROOF_CHANNEL, caption=caption)

    # Optionally: Perform OCR here to auto-detect payment details
    # image_path = await message.download()
    # data = await extract_payment_info(image_path)
    # valid = await validate_payment(data)

    await message.reply_text(
        text=screenshot_received_text,
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("📞 Contact Admin", url=f"https://t.me/{ADMIN_ID.replace('@', '')}"),
                InlineKeyboardButton("🧾 Tutorial", url=TUTORIAL_CHANNEL),
            ],
            [
                InlineKeyboardButton("🏠 Home", callback_data="go_home")
            ]
        ])
    )
