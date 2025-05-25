# bot/handlers/admin.py

from pyrogram import Client, filters
from pyrogram.types import Message
from config import ADMINS, TUTORIAL_URL_DB
from database.premium_db import add_premium_user, remove_premium_user
from utils.database import get_user_plan, set_tutorial_url, remove_tutorial_url
import os

# ✅ ADMIN CHECK
def admin_only(func):
    async def wrapper(client, message: Message):
        if message.from_user.id not in ADMINS:
            return await message.reply("🚫 You are not authorized to use this command.")
        return await func(client, message)
    return wrapper


# ✅ /add_premium user_id days
@Client.on_message(filters.command("add_premium") & filters.private)
@admin_only
async def add_premium_handler(client, message: Message):
    try:
        _, user_id, days = message.text.split()
        await add_premium_user(int(user_id), int(days))
        await message.reply(f"✅ User {user_id} added to premium for {days} days.")
    except Exception as e:
        await message.reply(f"❌ Usage: /add_premium user_id days\n\nError: {e}")

# ✅ /remove_premium user_id
@Client.on_message(filters.command("remove_premium") & filters.private)
@admin_only
async def remove_premium_handler(client, message: Message):
    try:
        _, user_id = message.text.split()
        await remove_premium_user(int(user_id))
        await message.reply(f"✅ Removed user {user_id} from premium.")
    except Exception as e:
        await message.reply(f"❌ Usage: /remove_premium user_id\n\nError: {e}")

# ✅ /id - get user & chat ID
@Client.on_message(filters.command("id"))
async def id_handler(client, message: Message):
    reply = message.reply_to_message
    user = reply.from_user if reply else message.from_user
    await message.reply(f"👤 User ID: `{user.id}`\n💬 Chat ID: `{message.chat.id}`")

# ✅ /restart
@Client.on_message(filters.command("restart") & filters.private)
@admin_only
async def restart_handler(client, message: Message):
    await message.reply("♻️ Bot is restarting...")
    os.execl(sys.executable, sys.executable, *sys.argv)

# ✅ /set_tutorial <url>
@Client.on_message(filters.command("set_tutorial") & filters.private)
@admin_only
async def set_tutorial(client, message: Message):
    try:
        url = message.text.split(maxsplit=1)[1]
        await set_tutorial_url(url)
        await message.reply("✅ Tutorial URL set successfully.")
    except IndexError:
        await message.reply("❌ Usage: /set_tutorial <url>")

# ✅ /remove_tutorial
@Client.on_message(filters.command("remove_tutorial") & filters.private)
@admin_only
async def remove_tutorial(client, message: Message):
    await remove_tutorial_url()
    await message.reply("✅ Tutorial URL removed.")

# ✅ /leave - Bot leaves the group (admin only)
@Client.on_message(filters.command("leave") & filters.group)
@admin_only
async def leave_group(client, message: Message):
    await message.reply("👋 Leaving this chat as requested by admin...")
    await client.leave_chat(message.chat.id)
