# bot/handlers/fsub.py

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import FORCE_SUB_CHANNELS, AUTO_APPROVE_FSUB
from database.user_db import approve_user
from utils.admins import is_admin

# 🔧 ForceSub Check Function
async def check_force_sub(client: Client, user_id: int):
    from pyrogram.errors import UserNotParticipant, ChatAdminRequired

    if not FORCE_SUB_CHANNELS:
        return True  # No FSUB needed

    for channel in FORCE_SUB_CHANNELS:
        try:
            member = await client.get_chat_member(chat_id=channel, user_id=user_id)
            if member.status not in ("member", "administrator", "creator"):
                raise UserNotParticipant
        except UserNotParticipant:
            return channel  # User not subscribed
        except ChatAdminRequired:
            continue  # Bot not admin in channel

    # ✅ Auto-approve if enabled
    if AUTO_APPROVE_FSUB:
        await approve_user(user_id)

    return True  # All FSUB passed

# 🧪 Command to test FSUB manually
@Client.on_message(filters.command("check_fsub"))
async def manual_fsub_check(client, message: Message):
    user_id = message.from_user.id
    check = await check_force_sub(client, user_id)
    if check is True:
        return await message.reply("✅ You have joined all required channels.")
    else:
        btn = InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔔 Join Channel", url=f"https://t.me/{check}")],
             [InlineKeyboardButton("✅ I've Joined", callback_data="verify_fsub")]]
        )
        await message.reply("🚫 Please join the required channel to continue:", reply_markup=btn)

# ✅ Callback to recheck after user joins
@Client.on_callback_query(filters.regex("verify_fsub"))
async def fsub_verify_callback(client, callback):
    user_id = callback.from_user.id
    check = await check_force_sub(client, user_id)
    if check is True:
        await callback.message.edit_text("✅ Thank you! You're verified.")
    else:
        await callback.message.edit_text("🚫 Still not joined. Please join and try again.")

# 🛠 Admin Command: Toggle FSUB Auto-Approve
@Client.on_message(filters.command("toggle_fsub_auto") & filters.user(is_admin))
async def toggle_fsub_auto(client, message: Message):
    from config import toggle_auto_approve_fsub
    state = toggle_auto_approve_fsub()
    await message.reply(f"⚙️ Auto-Approve FSUB is now {'Enabled ✅' if state else 'Disabled ❌'}.")
