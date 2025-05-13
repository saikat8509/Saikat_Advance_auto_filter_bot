# bot/handlers/trending.py

from pyrogram import Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import TRENDING_CHANNEL_ID, MOVIE_GROUP_LINK
from utils.imdb import get_imdb_info
from utils.formatters import build_imdb_caption
from database.core import get_movie_by_file_id


async def post_to_trending(bot: Client, file_id: str):
    """
    Posts a trending movie to the trending channel with IMDb info and redirect button.
    """

    movie = await get_movie_by_file_id(file_id)
    if not movie:
        return

    title = movie.get("file_name")
    imdb_id = movie.get("imdb_id")
    caption = f"🎬 **{title}**\n"

    if imdb_id:
        imdb_data = await get_imdb_info(imdb_id)
        if imdb_data:
            caption += build_imdb_caption(imdb_data)

    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("🎥 Movie Link", url=MOVIE_GROUP_LINK)]
    ])

    try:
        await bot.send_message(
            chat_id=TRENDING_CHANNEL_ID,
            text=caption,
            reply_markup=buttons,
            disable_web_page_preview=True
        )
    except Exception as e:
        print(f"[TRENDING_POST_ERROR] {e}")

