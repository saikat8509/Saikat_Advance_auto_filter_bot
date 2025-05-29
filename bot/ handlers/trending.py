from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from bot.utils.database import get_trending_keywords
from config import TRENDING_CHANNEL_ID

TRENDING_LIMIT = 10  # Number of top trending keywords to show

@Client.on_message(filters.command(["trending"]))
async def trending_handler(client: Client, message: Message):
    trending_keywords = await get_trending_keywords(limit=TRENDING_LIMIT)

    if not trending_keywords:
        return await message.reply("🚫 No trending data available at the moment.")

    caption = "**🔥 Top Trending Searches:**\n\n"
    for i, (keyword, count) in enumerate(trending_keywords, start=1):
        caption += f"🔹 {i}. `{keyword}` — {count} searches\n"

    buttons = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("🔁 Refresh", callback_data="refresh_trending")],
            [InlineKeyboardButton("📢 Channel", url=f"https://t.me/{TRENDING_CHANNEL_ID.lstrip('@')}")]
        ]
    )

    await message.reply(caption, reply_markup=buttons)

@Client.on_callback_query(filters.regex("refresh_trending"))
async def refresh_trending_callback(client, callback_query):
    trending_keywords = await get_trending_keywords(limit=TRENDING_LIMIT)

    if not trending_keywords:
        return await callback_query.answer("🚫 No data to refresh.", show_alert=True)

    caption = "**🔥 Refreshed Trending Searches:**\n\n"
    for i, (keyword, count) in enumerate(trending_keywords, start=1):
        caption += f"🔹 {i}. `{keyword}` — {count} searches\n"

    buttons = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("🔁 Refresh", callback_data="refresh_trending")],
            [InlineKeyboardButton("📢 Channel", url=f"https://t.me/{TRENDING_CHANNEL_ID.lstrip('@')}")]
        ]
    )

    await callback_query.message.edit_text(caption, reply_markup=buttons)
    await callback_query.answer("🔄 Trending list updated!")
