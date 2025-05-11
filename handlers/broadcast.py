# handlers/broadcast.py

from pyrogram import filters, Client
from pyrogram.types import Message
from database.user_data import get_all_users, get_all_groups
from utils.helpers import send_batch_messages
from config import ADMINS

# Broadcast to all users
@Client.on_message(filters.command("ubroadcast") & filters.user(ADMINS))
async def user_broadcast_handler(client, message: Message):
    if not message.reply_to_message:
        return await message.reply("Reply to a message to broadcast.")
    
    msg = message.reply_to_message
    users = await get_all_users()
    total = len(users)

    success, failed = await send_batch_messages(client, users, msg)
    
    await message.reply(
        f"👥 User Broadcast Complete.\n✅ Success: {success}\n❌ Failed: {failed}\n📦 Total: {total}"
    )

# Broadcast to all groups
@Client.on_message(filters.command("gbroadcast") & filters.user(ADMINS))
async def group_broadcast_handler(client, message: Message):
    if not message.reply_to_message:
        return await message.reply("Reply to a message to broadcast.")
    
    msg = message.reply_to_message
    groups = await get_all_groups()
    total = len(groups)

    success, failed = await send_batch_messages(client, groups, msg)
    
    await message.reply(
        f"👥 Group Broadcast Complete.\n✅ Success: {success}\n❌ Failed: {failed}\n📦 Total: {total}"
    )

