# bot/handlers/filter.py

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from database.premium_db import is_premium_user
from database.files_db import search_files, increment_view_count
from database.trending_db import update_search_stats
from utils.shortener import generate_short_link
from utils.token import generate_token
from utils.template import generate_imdb_template
from config import TUTORIAL_CHANNEL_LINK

@Client.on_message(filters.text & filters.private)
async def autofilter_handler(client: Client, message: Message):
    user_id = message.from_user.id
    query = message.text.strip()

    # 🔍 Update trending stats
    await update_search_stats(query)

    # 🎬 Search matching files in DB
    files = await search_files(query)

    if not files:
        return await message.reply("❌ No matching results found.")

    is_premium = await is_premium_user(user_id)
    buttons = []

    for file in files:
        file_id = file['file_id']
        file_name = file['file_name']
        await increment_view_count(file_id)

        if is_premium:
            url = f"https://t.me/{client.me.username}?start=dl_{file_id}"
        else:
            token = generate_token(file_id, user_id)
            url = await generate_short_link(f"https://t.me/{client.me.username}?start={token}")

        buttons.append([InlineKeyboardButton(file_name[:60], url=url)])

    # 🧾 Add additional buttons for non-premium
    if not is_premium:
        buttons.insert(0, [InlineKeyboardButton("🔥 Buy Premium Membership", callback_data="premium_menu")])
        buttons.append([InlineKeyboardButton("❓ How To Download", url=TUTORIAL_CHANNEL_LINK)])

    # 🎞 Optional: Include IMDb template above result if available
    imdb_template = await generate_imdb_template(query)
    caption = imdb_template if imdb_template else f"🎬 **Search Results for:** `{query}`"

    await message.reply(
        caption,
        reply_markup=InlineKeyboardMarkup(buttons),
        disable_web_page_preview=True
    )
