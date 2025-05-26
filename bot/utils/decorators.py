# bot/utils/decorators.py

from functools import wraps
from pyrogram.types import Message
from pyrogram.enums import ChatType
from config import ADMINS, FORCE_SUB_CHANNELS
from bot.utils.database import is_premium, add_user, create_referral, get_required_channels
from pyrogram.errors import UserNotParticipant

from pyrogram import Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# === ADMIN ONLY ===

def admin_only(func):
    @wraps(func)
    async def wrapper(client: Client, message: Message, *args, **kwargs):
        if message.from_user.id not in ADMINS:
            return await message.reply_text("🚫 You are not authorized to use this command.")
        return await func(client, message, *args, **kwargs)
    return wrapper

# === PREMIUM USER ONLY ===

def premium_only(func):
    @wraps(func)
    async def wrapper(client: Client, message: Message, *args, **kwargs):
        if await is_premium(message.from_user.id):
            return await func(client, message, *args, **kwargs)
        await message.reply_text(
            "**🔒 This feature is for premium users only.**\n\n👉 Upgrade your plan from the button below.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("💎 Premium Plans", callback_data="premium_plans")],
                    [InlineKeyboardButton("👥 Referral Program", callback_data="referral")],
                ]
            )
        )
    return wrapper

# === FORCE SUBSCRIBE CHECK ===

def force_subscribe(func):
    @wraps(func)
    async def wrapper(client: Client, message: Message, *args, **kwargs):
        if message.chat.type != ChatType.PRIVATE:
            return await func(client, message, *args, **kwargs)

        required_channels = await get_required_channels()

        if not required_channels:
            return await func(client, message, *args, **kwargs)

        for ch in required_channels:
            try:
                member = await client.get_chat_member(ch, message.from_user.id)
                if member.status in ("left", "kicked"):
                    raise UserNotParticipant
            except UserNotParticipant:
                return await message.reply_text(
                    "🔒 You must join our update channels to use the bot!",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [InlineKeyboardButton("📢 Join Channel", url=f"https://t.me/{ch.strip('@')}")],
                            [InlineKeyboardButton("✅ I Joined", callback_data="check_fsub")]
                        ]
                    )
                )
            except Exception:
                pass  # continue checking next channel

        return await func(client, message, *args, **kwargs)
    return wrapper

# === USER REGISTRATION + REFERRAL ===

def register_user(func):
    @wraps(func)
    async def wrapper(client: Client, message: Message, *args, **kwargs):
        user_id = message.from_user.id
        name = message.from_user.first_name
        await add_user(user_id, name)
        await create_referral(user_id)
        return await func(client, message, *args, **kwargs)
    return wrapper
