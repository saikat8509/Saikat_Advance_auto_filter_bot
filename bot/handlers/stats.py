# bot/handlers/stats.py

from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import (
    ADMINS, MONGODB_URIS, MOVIE_GROUP_LINK,
    UPDATES_CHANNEL_LINK, BACKUP_GROUP_LINK
)
from database.core import get_db_stats_for_all_uris

stats_router = Router()

@stats_router.message(Command("stats"))
async def stats_handler(message: types.Message):
    user_id = str(message.from_user.id)
    if user_id not in ADMINS:
        return await message.reply("❌ You are not authorized to use this command.")

    # 🧮 Get stats from MongoDB across multiple URIs
    stats_text = "<b>📊 Database Stats:</b>\n\n"
    total_files = 0

    for i, uri in enumerate(MONGODB_URIS, start=1):
        stat = await get_db_stats_for_all_uris(uri)
        stats_text += (
            f"🗂 <b>MongoDB {i}:</b>\n"
            f"├ Total Files Indexed: <code>{stat['total_files']}</code>\n"
            f"├ Storage Used: <code>{stat['storage_used']} MB</code>\n"
            f"└ Storage Available: <code>{stat['storage_free']} MB</code>\n\n"
        )
        total_files += stat['total_files']

    stats_text += f"<b>🔢 Total Indexed Files:</b> <code>{total_files}</code>"

    # 🔘 Button UI
    buttons = [
        [InlineKeyboardButton(text="🎬 Movie Group", url=MOVIE_GROUP_LINK)],
        [InlineKeyboardButton(text="📢 Updates Channel", url=UPDATES_CHANNEL_LINK)],
        [InlineKeyboardButton(text="🔁 Backup Group", url=BACKUP_GROUP_LINK)],
    ]

    await message.answer(stats_text, reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))

