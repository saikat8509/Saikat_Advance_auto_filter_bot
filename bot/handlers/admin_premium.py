# bot/handlers/admin_premium.py

from pyrogram import Client, filters
from pyrogram.types import Message
from config import AUTH_USERS, LOG_CHANNEL_ID
from database.users import set_premium, remove_premium, get_user_info
from datetime import datetime
import re

@Client.on_message(filters.command("add_premium") & filters.user(AUTH_USERS))
async def add_premium_handler(bot: Client, message: Message):
    if len(message.command) < 3:
        return await message.reply("Usage: `/add_premium <user_id> <days>`", quote=True)

    try:
        user_id = int(message.command[1])
        days = int(message.command[2])
    except ValueError:
        return await message.reply("Invalid format. Use: `/add_premium <user_id> <days>`", quote=True)

    set_premium(user_id, days)
    user_info = get_user_info(user_id)
    expiry = user_info.get("premium_expiry")

    await message.reply(
        f"✅ Premium access granted to `{user_id}` for `{days}` days.\n"
        f"⏰ Expires on: `{expiry.strftime('%Y-%m-%d %H:%M:%S')} UTC`"
    )

    try:
        await bot.send_message(
            user_id,
            f"🎉 You’ve been granted Premium Access for {days} days!\n"
            f"Enjoy ad-free direct downloads.\n"
            f"⏳ Expires: `{expiry.strftime('%Y-%m-%d %H:%M:%S')} UTC`"
        )
    except Exception:
        pass

    if LOG_CHANNEL_ID:
        await bot.send_message(
            LOG_CHANNEL_ID,
            f"✅ Premium Added\n\n"
            f"👤 User ID: `{user_id}`\n"
            f"🕐 Days: {days}\n"
            f"⏳ Expiry: `{expiry.strftime('%Y-%m-%d %H:%M:%S')} UTC`"
        )


@Client.on_message(filters.command("remove_premium") & filters.user(AUTH_USERS))
async def remove_premium_handler(bot: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply("Usage: `/remove_premium <user_id>`", quote=True)

    try:
        user_id = int(message.command[1])
    except ValueError:
        return await message.reply("Invalid user ID. Use: `/remove_premium <user_id>`", quote=True)

    remove_premium(user_id)
    await message.reply(f"🚫 Removed premium access for `{user_id}`")

    try:
        await bot.send_message(
            user_id,
            "⚠️ Your premium access has been removed. You now see shortener links for downloads."
        )
    except Exception:
        pass

    if LOG_CHANNEL_ID:
        await bot.send_message(
            LOG_CHANNEL_ID,
            f"🚫 Premium Removed\n\n"
            f"👤 User ID: `{user_id}`"
        )
