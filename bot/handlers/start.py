from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from config import (
    START_IMAGES,
    UPDATE_CHANNEL_URL,
    MOVIE_GROUP_URL,
    SUPPORT_GROUP_URL,
    TUTORIAL_CHANNEL_URL,
    PAYMENT_PROOF_CHANNEL_URL
)
from bot.utils.database import db

# Track rotating image index per user (in-memory)
user_image_index = {}

@Client.on_message(filters.command("start") & filters.private)
async def start_command(client: Client, message: Message):
    user_id = message.from_user.id
    username = message.from_user.username or "NoUsername"

    # Register user if new
    await db.add_user(user_id, username)

    # Referral handling
    if len(message.command) > 1:
        ref_code = message.command[1]
        if ref_code.isdigit() and int(ref_code) != user_id:
            await db.add_referral(int(ref_code), user_id)

    # Handle rotating image
    image_list = START_IMAGES
    total = len(image_list)
    index = user_image_index.get(user_id, 0)
    image_url = image_list[index]
    user_image_index[user_id] = (index + 1) % total

    caption = f"""👋 **Welcome {message.from_user.mention}**

🚀 I'm your all-in-one Movie Autofilter Bot with:
• Direct downloads for premium users
• IMDb-based movie search
• Token verification for safe access
• Referral rewards system
• AI screenshot verification for payments

💎 Use the buttons below to explore more!
"""

    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("⚒️ ADD ME TO YOUR GROUP ⚒️", url="https://t.me/Princess_Surch_Bot?startgroup=true")],
        [
            InlineKeyboardButton("JOIN UPDATE CHANNEL", url=UPDATE_CHANNEL_URL),
            InlineKeyboardButton("MOVIE GROUP", url=MOVIE_GROUP_URL),
        ],
        [
            InlineKeyboardButton("SUPPORT GROUP", url=SUPPORT_GROUP_URL),
            InlineKeyboardButton("ABOUT", callback_data="about"),
        ],
        [
            InlineKeyboardButton("PREMIUM MEMBERSHIP & REFERRAL", callback_data="premium_info"),
        ],
        [
            InlineKeyboardButton("⚒️ Help Menu", callback_data="help_menu"),
        ],
    ])

    try:
        await message.reply_photo(
            photo=image_url,
            caption=caption,
            reply_markup=buttons
        )
    except Exception as e:
        await message.reply(f"❌ Failed to load welcome image.\n\nError: `{e}`")
