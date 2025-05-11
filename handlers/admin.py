from pyrogram import filters
from pyrogram.types import Message
from bot import Bot, Config
from database import user_db, chat_db, file_db
from utils.admin_check import admin_check
from utils.broadcast import broadcast_users, broadcast_groups
from utils.helpers import delete_camrip_predvd

@Bot.on_message(filters.command("ban") & filters.user(Config.ADMINS))
async def ban_user(_, message: Message):
    if len(message.command) < 2:
        return await message.reply("Provide a user ID to ban.")
    user_id = int(message.command[1])
    await user_db.ban_user(user_id)
    await message.reply(f"User {user_id} banned.")

@Bot.on_message(filters.command("unban") & filters.user(Config.ADMINS))
async def unban_user(_, message: Message):
    if len(message.command) < 2:
        return await message.reply("Provide a user ID to unban.")
    user_id = int(message.command[1])
    await user_db.unban_user(user_id)
    await message.reply(f"User {user_id} unbanned.")

@Bot.on_message(filters.command("leave") & filters.user(Config.ADMINS))
async def leave_chat(_, message: Message):
    if len(message.command) < 2:
        return await message.reply("Provide a chat ID or username.")
    chat_id = message.command[1]
    await Bot.leave_chat(chat_id)
    await message.reply(f"Left chat {chat_id}.")

@Bot.on_message(filters.command("disable") & filters.user(Config.ADMINS))
async def disable_chat(_, message: Message):
    if len(message.command) < 2:
        return await message.reply("Provide a chat ID to disable.")
    chat_id = int(message.command[1])
    await chat_db.disable_chat(chat_id)
    await message.reply(f"Chat {chat_id} disabled.")

@Bot.on_message(filters.command("broadcast") & filters.user(Config.ADMINS))
async def handle_broadcast(_, message: Message):
    if not message.reply_to_message:
        return await message.reply("Reply to a message to broadcast.")
    target = message.command[1] if len(message.command) > 1 else "all"

    if target == "users":
        await broadcast_users(message.reply_to_message)
    elif target == "groups":
        await broadcast_groups(message.reply_to_message)
    else:
        await broadcast_users(message.reply_to_message)
        await broadcast_groups(message.reply_to_message)

    await message.reply("Broadcast sent successfully.")

@Bot.on_message(filters.command("delete_camrip") & filters.user(Config.ADMINS))
async def handle_delete_camrip(_, message: Message):
    deleted_count = await delete_camrip_predvd()
    await message.reply(f"Deleted {deleted_count} PreDVD / CamRip files.")

@Bot.on_message(filters.command("stats") & filters.user(Config.ADMINS))
async def stats_handler(_, message: Message):
    users = await user_db.count_users()
    groups = await chat_db.count_chats()
    files = await file_db.count_files()
    await message.reply(f"👤 Users: {users}\n👥 Groups: {groups}\n📁 Files: {files}")

