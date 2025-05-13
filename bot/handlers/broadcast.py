# bot/handlers/broadcast.py

import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from config import ADMINS
from database.users import get_all_users
from utils.helpers import is_admin

BROADCAST_USAGE = "📢 <b>Usage:</b>\nReply to any message with <code>/broadcast</code> to send it to all users."

@Client.on_message(filters.command("broadcast") & filters.reply)
async def broadcast_handler(client: Client, message: Message):
    if not await is_admin(message.from_user.id):
        return await message.reply_text("🚫 You are not authorized to use this command.")

    reply_msg = message.reply_to_message
    if not reply_msg:
        return await message.reply_text(BROADCAST_USAGE)

    users = await get_all_users()
    total = len(users)
    success = 0
    failed = 0

    progress = await message.reply_text(f"📤 Broadcast started...\n\n✅ Success: {success}\n❌ Failed: {failed}\n👥 Total: {total}")

    for user in users:
        try:
            await reply_msg.copy(chat_id=user["_id"])
            success += 1
        except Exception:
            failed += 1
        await asyncio.sleep(0.1)

        if (success + failed) % 20 == 0:
            await progress.edit_text(f"📤 Broadcasting...\n\n✅ Success: {success}\n❌ Failed: {failed}\n👥 Total: {total}")

    await progress.edit_text(f"✅ Broadcast finished.\n\n✅ Success: {success}\n❌ Failed: {failed}\n👥 Total: {total}")

