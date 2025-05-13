# bot/handlers/admin_premium.py

from pyrogram import Client, filters
from pyrogram.types import Message
from config import AUTH_USERS
from database.users import set_premium, get_user_info

@Client.on_message(filters.command("add_premium") & filters.user(AUTH_USERS))
async def add_premium_command(bot: Client, message: Message):
    if len(message.command) < 3:
        return await message.reply_text("Usage:\n`/add_premium <user_id> <days>`")

    try:
        user_id = int(message.command[1])
        days = int(message.command[2])
        set_premium(user_id, days)
        await message.reply_text(f"✅ User `{user_id}` has been given premium for `{days}` days.")
    except Exception as e:
        await message.reply_text(f"⚠️ Error: {e}")

@Client.on_message(filters.command("remove_premium") & filters.user(AUTH_USERS))
async def remove_premium_command(bot: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("Usage:\n`/remove_premium <user_id>`")

    try:
        user_id = int(message.command[1])
        info = get_user_info(user_id)
        if info and info.get("is_premium"):
            set_premium(user_id, 0)
            await message.reply_text(f"✅ Premium removed from user `{user_id}`.")
        else:
            await message.reply_text(f"ℹ️ User `{user_id}` is not a premium member.")
    except Exception as e:
        await message.reply_text(f"⚠️ Error: {e}")
