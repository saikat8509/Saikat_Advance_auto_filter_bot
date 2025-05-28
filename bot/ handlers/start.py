from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import START_IMAGES, BOT_NAME, OWNER_USERNAME, UPDATE_CHANNEL_URL, MOVIE_GROUP_URL, SUPPORT_GROUP_URL, ABOUT_IMAGE_URL
from bot.utils.buttons import get_start_buttons
from bot.utils.database import get_user, save_user
import random

# Track rotating image index
image_index = {}


@Client.on_message(filters.private & filters.command("start"))
async def start_handler(client: Client, message: Message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name

    # Save user to DB if not exists
    await save_user(user_id, first_name)

    # Handle rotating image
    index = image_index.get(user_id, 0)
    image_url = START_IMAGES[index % len(START_IMAGES)]
    image_index[user_id] = index + 1

    caption = f"""👋 **Hello {first_name}!**
Welcome to **{BOT_NAME}** 🎬

I can help you search and download movies with lightning speed 🚀

Choose an option below to get started:
"""

    buttons = get_start_buttons()

    await message.reply_photo(
        photo=image_url,
        caption=caption,
        reply_markup=InlineKeyboardMarkup(buttons)
    )
