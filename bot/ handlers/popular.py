from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.database.popular import get_popular_files, get_trending_files, get_admin_picks
from bot.utils.helper import generate_file_card
from config import ADMINS

# 📈 /trending command: Show trending movies by download frequency
@Client.on_message(filters.command("trending") & filters.private)
async def show_trending_movies(client, message):
    files = await get_trending_files(limit=10)
    if not files:
        return await message.reply("⚠️ No trending movies found.")

    text = "🔥 **Top Trending Movies (by downloads):**\n\n"
    for idx, file in enumerate(files, start=1):
        text += f"{idx}. `{file['file_name']}` — 📥 {file['download_count']} downloads\n"
    await message.reply(text)

# ⭐ /popular command: Show most viewed/popular files
@Client.on_message(filters.command("popular") & filters.private)
async def show_popular_movies(client, message):
    files = await get_popular_files(limit=10)
    if not files:
        return await message.reply("⚠️ No popular movies found.")

    text = "⭐ **Most Popular Files (by views):**\n\n"
    for idx, file in enumerate(files, start=1):
        text += f"{idx}. `{file['file_name']}` — 👁️ {file['views']} views\n"
    await message.reply(text)

# 👑 /adminpicks command: Show admin-featured movies
@Client.on_message(filters.command("adminpicks") & filters.private)
async def show_admin_picks(client, message):
    files = await get_admin_picks(limit=10)
    if not files:
        return await message.reply("⚠️ No admin picks available.")

    text = "👑 **Editor's Picks (Admin Selected):**\n\n"
    for idx, file in enumerate(files, start=1):
        text += f"{idx}. `{file['file_name']}` — 🆔 `{file['file_id']}`\n"
    await message.reply(text)

# ✅ Admin command to feature a file as admin pick
@Client.on_message(filters.command("feature") & filters.private & filters.user(ADMINS))
async def feature_file_admin(client, message):
    if len(message.command) < 2:
        return await message.reply("⚠️ Provide the file_id to feature.\n\nUsage: `/feature <file_id>`")

    file_id = message.command[1]
    from bot.database.popular import mark_as_admin_pick
    success = await mark_as_admin_pick(file_id)

    if success:
        await message.reply("✅ File successfully marked as Admin Pick.")
    else:
        await message.reply("❌ Failed to mark file as Admin Pick.")

# 🔄 /refreshpopular: Admin-only command to manually recalculate trends/popular
@Client.on_message(filters.command("refreshpopular") & filters.private & filters.user(ADMINS))
async def refresh_popular_data(client, message):
    from bot.database.popular import refresh_popular_stats
    await refresh_popular_stats()
    await message.reply("♻️ Popular/trending stats refreshed.")

# 🔘 Button-based access for Trending & Popular
@Client.on_callback_query(filters.regex("show_popular"))
async def callback_popular(client, callback_query):
    files = await get_popular_files(limit=5)
    text = "⭐ **Popular Files:**\n\n" + "\n".join(
        [f"{i+1}. `{f['file_name']}` — 👁️ {f['views']} views" for i, f in enumerate(files)]
    )
    await callback_query.message.edit_text(
        text=text,
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="back_to_menu")]])
    )

@Client.on_callback_query(filters.regex("show_trending"))
async def callback_trending(client, callback_query):
    files = await get_trending_files(limit=5)
    text = "🔥 **Trending Downloads:**\n\n" + "\n".join(
        [f"{i+1}. `{f['file_name']}` — 📥 {f['download_count']} downloads" for i, f in enumerate(files)]
    )
    await callback_query.message.edit_text(
        text=text,
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Back", callback_data="back_to_menu")]])
    )
