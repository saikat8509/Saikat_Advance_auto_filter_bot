from pyrogram import filters
from pyrogram.types import Message
from config import AUTH_USERS
from database.users import set_premium, remove_premium
from bot import Bot


@Bot.on_message(filters.command("add_premium") & filters.user(AUTH_USERS))
async def add_premium_user(bot, message: Message):
    if len(message.command) < 3:
        return await message.reply_text("Usage: /add_premium <user_id> <days>")

    try:
        user_id = int(message.command[1])
        days = int(message.command[2])
        set_premium(user_id, days)
        await message.reply_text(f"✅ User `{user_id}` has been added to premium for {days} days.")
    except Exception as e:
        await message.reply_text(f"❌ Error: {e}")


@Bot.on_message(filters.command("remove_premium") & filters.user(AUTH_USERS))
async def remove_premium_user(bot, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("Usage: /remove_premium <user_id>")

    try:
        user_id = int(message.command[1])
        remove_premium(user_id)
        await message.reply_text(f"✅ Premium removed for user `{user_id}`.")
    except Exception as e:
        await message.reply_text(f"❌ Error: {e}")
