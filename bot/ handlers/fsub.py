from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import FORCE_SUB_CHANNELS, AUTO_APPROVE_FSUB
from bot.utils.database import is_user_subscribed
from pyrogram.errors import UserNotParticipant, ChannelPrivate

async def check_force_subscribe(client: Client, message: Message):
    if not FORCE_SUB_CHANNELS:
        return True  # No channels to force subscribe

    for channel in FORCE_SUB_CHANNELS:
        try:
            user = await client.get_chat_member(channel, message.from_user.id)
            if user.status in ("member", "administrator", "creator"):
                return True if AUTO_APPROVE_FSUB else None
        except UserNotParticipant:
            continue
        except ChannelPrivate:
            continue
        except Exception:
            continue

    # Not subscribed to any required channel
    buttons = [
        [InlineKeyboardButton("📢 Join Update Channel", url=f"https://t.me/{FORCE_SUB_CHANNELS[0].lstrip('@')}")],
        [InlineKeyboardButton("✅ I've Joined", callback_data="check_fsub")]
    ]
    await message.reply_text(
        "🚫 To use this bot, you must join our update channel first!",
        reply_markup=InlineKeyboardMarkup(buttons),
        disable_web_page_preview=True
    )
    return False

@Client.on_callback_query(filters.regex("check_fsub"))
async def recheck_fsub(client, callback_query):
    user_id = callback_query.from_user.id
    ok = False

    for channel in FORCE_SUB_CHANNELS:
        try:
            member = await client.get_chat_member(channel, user_id)
            if member.status in ("member", "administrator", "creator"):
                ok = True
                break
        except Exception:
            continue

    if ok:
        await callback_query.message.edit_text("✅ You’ve successfully joined. You can now use the bot.")
    else:
        await callback_query.answer("❌ You still haven't joined the channel.", show_alert=True)
