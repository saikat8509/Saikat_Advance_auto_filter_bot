import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from bot.utils.imdb import search_imdb, get_imdb_details
from bot.utils.buttons import back_button
from bot.utils.database import update_search_count
from bot.utils.texts import build_imdb_caption


@Client.on_message(filters.command("imdb"))
async def imdb_search_handler(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply("🔎 Usage: `/imdb movie name`", quote=True)
    
    query = message.text.split(None, 1)[1]
    results = await search_imdb(query)
    
    if not results:
        return await message.reply("❌ No results found on IMDb.")
    
    buttons = [
        [InlineKeyboardButton(f"{movie['title']} ({movie['year']})", callback_data=f"imdb_{movie['id']}")]
        for movie in results[:5]
    ]
    buttons.append([InlineKeyboardButton("❌ Close", callback_data="close")])
    
    await message.reply("🎬 Select a title from the results below:", reply_markup=InlineKeyboardMarkup(buttons))


@Client.on_callback_query(filters.regex(r"^imdb_(tt\d+)"))
async def imdb_details_handler(client, callback_query):
    imdb_id = callback_query.data.split("_")[1]
    await callback_query.answer("Fetching IMDb info...", show_alert=False)

    movie = await get_imdb_details(imdb_id)
    if not movie:
        return await callback_query.edit_message_text("❌ Could not fetch IMDb details.")

    await update_search_count(movie.get("title"))

    caption = build_imdb_caption(movie)
    image_url = movie.get("poster") or "https://graph.org/file/default.jpg"
    
    buttons = [
        [
            InlineKeyboardButton("🌐 View on IMDb", url=f"https://www.imdb.com/title/{imdb_id}"),
            InlineKeyboardButton("🔙 Back", callback_data="back_to_search")
        ]
    ]

    try:
        await callback_query.message.delete()
        await client.send_photo(
            chat_id=callback_query.message.chat.id,
            photo=image_url,
            caption=caption,
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    except Exception:
        await callback_query.message.edit_text(caption, reply_markup=InlineKeyboardMarkup(buttons))


@Client.on_callback_query(filters.regex("back_to_search"))
async def go_back_to_search(client, callback_query):
    await callback_query.answer("Going back...", show_alert=False)
    # Cannot recover search list – better to tell the user
    await callback_query.edit_message_text("🔎 Please send /imdb <movie name> again to search.")


@Client.on_callback_query(filters.regex("close"))
async def close_button_handler(client, callback_query):
    await callback_query.message.delete()
