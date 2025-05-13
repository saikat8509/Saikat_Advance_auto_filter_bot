# bot/handlers/plans.py

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from config import (
    ADMINS,
    PLAN_DETAILS_TEXT,
    UPI_ID,
    PAYMENT_QR_CODE_URL,
    PREMIUM_STICKER_URL,
    REFERRAL_REWARD_DAYS
)

@Client.on_message(filters.command("plan"))
async def show_premium_plan(client: Client, message: Message):
    buttons = [
        [
            InlineKeyboardButton("💸 PAY NOW", url=f"https://t.me/{client.me.username}?start=buy")
        ],
        [
            InlineKeyboardButton("🎁 CLAIM VIA REFERRAL", url=f"https://t.me/{client.me.username}?start=refer")
        ]
    ]

    text = PLAN_DETAILS_TEXT.format(
        upi=UPI_ID,
        days=REFERRAL_REWARD_DAYS
    )

    if PAYMENT_QR_CODE_URL:
        try:
            await client.send_photo(
                chat_id=message.chat.id,
                photo=PAYMENT_QR_CODE_URL,
                caption=text,
                reply_markup=InlineKeyboardMarkup(buttons)
            )
        except Exception as e:
            await message.reply_text(f"❌ Failed to send QR code. Error:\n<code>{e}</code>")
    else:
        await message.reply_text(
            text=text,
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    # Send optional sticker
    if PREMIUM_STICKER_URL:
        try:
            await client.send_sticker(message.chat.id, PREMIUM_STICKER_URL)
        except Exception:
            pass  # Ignore if sticker fails
