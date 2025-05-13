# bot/handlers/start.py

from aiogram import Router, types, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
from aiogram.filters import CommandStart
from config import (
    BOT_USERNAME, START_IMAGE_URL, BUY_PREMIUM_TEXT, ADMINS,
    MOVIE_GROUP_LINK, UPDATES_CHANNEL_LINK, BACKUP_GROUP_LINK
)

start_router = Router()

@start_router.message(CommandStart())
async def start_handler(message: Message):
    user_id = message.from_user.id

    # 🧲 Build main buttons
    buttons = [
        [InlineKeyboardButton(text="🎬 Movie Group", url=MOVIE_GROUP_LINK)],
        [InlineKeyboardButton(text="📢 Updates Channel", url=UPDATES_CHANNEL_LINK)],
        [InlineKeyboardButton(text="🔁 Backup Group", url=BACKUP_GROUP_LINK)],
        [InlineKeyboardButton(text="💎 Buy Premium Membership", callback_data="buy_premium")],
        [InlineKeyboardButton(text="ℹ️ About", callback_data="about")]
    ]

    # 👑 Admin-only help button
    if str(user_id) in ADMINS:
        buttons.append([InlineKeyboardButton(text="🛠 Help", callback_data="help")])

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    caption = (
        f"👋 Hello, {message.from_user.mention()}!\n\n"
        f"Welcome to <b>{BOT_USERNAME}</b>.\n\n"
        f"🔍 I can help you find and download your favorite movies from our database.\n\n"
        f"💎 Use the button below to upgrade to premium and enjoy ad-free downloads.\n"
    )

    try:
        # Send image with caption and buttons
        await message.answer_photo(photo=START_IMAGE_URL, caption=caption, reply_markup=keyboard)
    except Exception as e:
        # Fallback if image fails to send
        await message.answer(caption, reply_markup=keyboard)

