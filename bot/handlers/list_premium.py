# bot/handlers/list_premium.py

from pyrogram import Client, filters
from pyrogram.types import Message
from config import AUTH_USERS
from database.users import get_all_premium_users
from datetime import datetime

@Client.on_message(filters.command("list_premium") & filters.user(AUTH_USERS))
async def list_premium_users(bot: Client, message: Message):
    users = get_all_premium_users()
    if not users:
        return await message.reply("No premium users found.")

    text = "**💎 Active Premium Users:**\n\n"
    for user in users:
        user_id = user['user_id']
        expiry = user.get("premium_expiry")
        expiry_str = expiry.strftime('%Y-%m-%d %H:%M:%S') if expiry else "Unknown"
        text += f"• `{user_id}` → Expires: `{expiry_str} UTC`\n"

    if len(text) > 4096:
        # Send as file if too long
        with open("premium_users.txt", "w") as f:
            f.write(text)
        await message.reply_document("premium_users.txt")
    else:
        await message.reply(text)
