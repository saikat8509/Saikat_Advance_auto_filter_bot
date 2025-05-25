import asyncio
from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import ADMINS
from bot.utils.imdb_scraper import get_imdb_details
from bot.utils.helper import format_imdb_caption, extract_imdb_id
from bot.database.recent_searches import save_recent_search

@Client.on_message(filters.command("imdb") & filters.private)
async def imdb_search_handler(client, message):
    if len(message.command) < 2:
        return await message.reply("Please provide a movie or series name.\n\nUsage: `/imdb Inception`")

    query = message.text.split(" ", 1)[1]
    await message.reply_chat_action("typing")
    
    try:
        imdb_data = await get_imdb_details(query)
        if not imdb_data:
            return await message.reply("No IMDb results found. Please try a different name.")

        await save_recent_search(message.from_user.id, imdb_data["title"])

        caption = format_imdb_caption(imdb_data)
        imdb_id = extract_imdb_id(imdb_data["url"])
        buttons = [
            [InlineKeyboardButton("📺 Trailer", url=imdb_data["trailer_url"])] if imdb_data.get("trailer_url") else [],
            [InlineKeyboardButton("🔗 IMDb Link", url=imdb_data["url"])],
            [InlineKeyboardButton("🗂️ Genres", callback_data=f"genres_{imdb_id}")],
            [InlineKeyboardButton("🔙 Back", callback_data="back_to_menu")]
        ]
        return await message.reply_photo(imdb_data["poster"], caption=caption, reply_markup=InlineKeyboardMarkup(buttons))

    except Exception as e:
        return await message.reply(f"Error fetching IMDb data:\n`{e}`")

@Client.on_message(filters.command("imdbid") & filters.private & filters.user(ADMINS))
async def get_imdbid_from_url(client, message):
    if len(message.command) < 2:
        return await message.reply("Please provide a full IMDb URL.\n\nUsage: `/imdbid https://www.imdb.com/title/tt1375666/`")

    url = message.command[1]
    imdb_id = extract_imdb_id(url)
    if imdb_id:
        await message.reply(f"✅ Extracted IMDb ID: `{imdb_id}`")
    else:
        await message.reply("⚠️ Invalid IMDb URL.")

@Client.on_message(filters.command("genimdb") & filters.private & filters.user(ADMINS))
async def generate_imdb_card(client, message):
    if len(message.command) < 2:
        return await message.reply("Provide an IMDb ID or title to generate the card.\n\nExample: `/genimdb tt1375666` or `/genimdb Inception`")

    query = message.text.split(" ", 1)[1]
    await message.reply_chat_action("upload_photo")
    
    try:
        imdb_data = await get_imdb_details(query)
        if not imdb_data:
            return await message.reply("Failed to fetch IMDb data.")

        caption = format_imdb_caption(imdb_data)
        await message.reply_photo(imdb_data["poster"], caption=caption)
    except Exception as e:
        await message.reply(f"Failed to generate IMDb card:\n`{e}`")

@Client.on_message(filters.command("imdbinline") & filters.private)
async def imdb_inline_prompt(client, message):
    await message.reply("Use inline mode to search IMDb:\n`@YourBotUsername Inception`")

# Callback handler for genre info
@Client.on_callback_query(filters.regex(r"genres_(tt\d+)"))
async def genre_info_callback(client, callback_query):
    imdb_id = callback_query.data.split("_", 1)[1]
    try:
        imdb_data = await get_imdb_details(imdb_id)
        genres = imdb_data.get("genres", "Not available")
        await callback_query.message.edit_caption(
            caption=f"🎬 **Genres for {imdb_data['title']}**\n\n`{genres}`",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Back", callback_data="back_to_menu")]
            ])
        )
    except Exception as e:
        await callback_query.answer("Error retrieving genre info.", show_alert=True)

# Handle "Back to menu"
@Client.on_callback_query(filters.regex("back_to_menu"))
async def back_to_main_menu(client, callback_query):
    await callback_query.message.edit_text("🔙 Back to main menu. Use /start to begin again.")

