from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from config import (
    START_IMAGES, UPDATE_CHANNEL, MOVIE_GROUP, SUPPORT_GROUP,
    OWNER_USERNAME, TUTORIAL_CHANNEL
)
from bot.utils.database import db

# In-memory image rotation index for each user (reset every session)
user_image_index = {}

@Client.on_message(filters.command("start") & filters.private)
async def start_private(client: Client, message: Message):
    user_id = message.from_user.id
    username = message.from_user.username or "NoUsername"

    # Register user if new
    await db.add_user(user_id, username)

    # Handle referral system
    if len(message.command) > 1:
        ref_code = message.command[1]
        if ref_code.isdigit() and int(ref_code) != user_id:
            await db.add_referral(int(ref_code), user_id)

    # Select next image for this user
    total_images = len(START_IMAGES)
    current_index = user_image_index.get(user_id, 0)
    image_url = START_IMAGES[current_index]
    user_image_index[user_id] = (current_index + 1) % total_images

    caption = f"""👋 **Welcome {message.from_user.mention}**

🚀 I'm your powerful Movie Autofilter Bot!

✨ Features:
• Direct downloads for Premium users
• Token verification for non-premium
• IMDb search integration
• AI payment screenshot verification
• Referral rewards & trials
• Trending & Popular movie sections

💎 Tap a button below to get started!
"""

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("⚒️ ADD ME TO YOUR GROUP ⚒️", url="https://t.me/Princess_Surch_Bot?startgroup=true")],
        [
            InlineKeyboardButton("JOIN UPDATE CHANNEL", url=UPDATE_CHANNEL),
            InlineKeyboardButton("MOVIE GROUP", url=MOVIE_GROUP)
        ],
        [
            InlineKeyboardButton("SUPPORT GROUP", url=SUPPORT_GROUP),
            InlineKeyboardButton("ABOUT", callback_data="about")
        ],
        [
            InlineKeyboardButton("PREMIUM MEMBERSHIP & REFERRAL", callback_data="premium_info")
        ],
        [
            InlineKeyboardButton("⚒️ Help Menu", callback_data="help_menu")
        ]
    ])

    try:
        await message.reply_photo(
            photo=image_url,
            caption=caption,
            reply_markup=keyboard
        )
    except Exception as e:
        await message.reply(f"⚠️ Failed to send start image.\n\nError: `{e}`")
