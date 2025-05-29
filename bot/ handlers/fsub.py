from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant, UserKicked, ChatAdminRequired, ChannelPrivate
from config import FORCE_SUB_CHANNELS, AUTO_APPROVE_FSUB


async def check_force_subscribe(client: Client, message: Message) -> bool:
    user_id = message.from_user.id

    for channel in FORCE_SUB_CHANNELS:
        try:
            member = await client.get_chat_member(channel, user_id)
            if member.status in ["member", "administrator", "creator"]:
                if AUTO_APPROVE_FSUB:
                    return True
        except UserNotParticipant:
            continue  # Not joined, try next
        except (UserKicked, ChannelPrivate, ChatAdminRequired):
            continue  # Skip inaccessible or blocked channels
        except Exception:
            continue  # Unknown error, proceed to next

    # If reached here, user hasn't joined any required channels
    join_buttons = [
        [InlineKeyboardButton(f"📢 JOIN {i+1}", url=f"https://t.me/{channel.lstrip('@')}")]
        for i, channel in enumerate(FORCE_SUB_CHANNELS)
    ]

    join_buttons.append([
        InlineKeyboardButton("✅ I've Joined", callback_data="check_fsub")
    ])

    await message.reply_text(
        "🔒 **Access Restricted!**\n\n"
        "To use this bot, please join at least one of the required update channels below.",
        reply_markup=InlineKeyboardMarkup(join_buttons),
        disable_web_page_preview=True
    )
    return False


@Client.on_callback_query(filters.regex("check_fsub"))
async def recheck_fsub(client, callback_query):
    message = callback_query.message
    user = callback_query.from_user

    for channel in FORCE_SUB_CHANNELS:
        try:
            member = await client.get_chat_member(channel, user.id)
            if member.status in ["member", "administrator", "creator"]:
                await callback_query.answer("✅ Access granted!", show_alert=True)
                return await message.delete()
        except:
            continue

    await callback_query.answer("❌ You're still not subscribed to any required channels.", show_alert=True)
