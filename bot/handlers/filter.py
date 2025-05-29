import re
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import DATABASE_CHANNEL_IDS, ENABLE_TOKEN_VERIFICATION, TUTORIAL_CHANNEL_URL
from bot.utils.database import is_premium_user, update_trending_query
from bot.utils.token import create_shortened_link
from bot.utils.buttons import get_premium_button
from config import PREMIUM_HEADER

FILE_EXTENSIONS = [".mkv", ".mp4", ".avi"]

@Client.on_message(filters.text & ~filters.private & ~filters.via_bot)
async def autofilter_handler(client: Client, message: Message):
    query = message.text.strip()
    if len(query) < 3:
        return  # Ignore short queries

    user_id = message.from_user.id
    is_premium = await is_premium_user(user_id)

    # Update trending stats
    await update_trending_query(query)

    # Search in all DB channels
    matched_files = []
    pattern = re.compile(fr".*{re.escape(query)}.*", re.IGNORECASE)

    for channel_id in DATABASE_CHANNEL_IDS:
        try:
            async for msg in client.search_messages(channel_id, query):
                if msg.document and any(msg.document.file_name.endswith(ext) for ext in FILE_EXTENSIONS):
                    if pattern.search(msg.document.file_name):
                        matched_files.append(msg)
        except Exception as e:
            print(f"Error in DB Channel {channel_id}: {e}")
            continue

    if not matched_files:
        await message.reply_text("❌ No matching files found.")
        return

    # Limit results to avoid flooding
    matched_files = matched_files[:20]

    # Send messages based on premium status
    if is_premium:
        for file_msg in matched_files:
            try:
                await file_msg.copy(chat_id=message.chat.id, reply_to_message_id=message.id)
            except Exception as e:
                print(f"Error copying message: {e}")
    else:
        for file_msg in matched_files:
            file_name = file_msg.document.file_name
            short_link = await create_shortened_link(client, user_id, file_msg.link) if ENABLE_TOKEN_VERIFICATION else file_msg.link

            text = f"**🎬 File:** `{file_name}`\n\n**🔥 Buy premium membership to unlock full access!**"
            buttons = [
                [
                    InlineKeyboardButton("🔓 Download Now", url=short_link),
                    InlineKeyboardButton("📥 How To Download", url=TUTORIAL_CHANNEL_URL),
                ],
                get_premium_button()
            ]

            await message.reply_photo(
                photo="https://graph.org/file/80e96b21559c7d19e51ec.jpg",
                caption=text,
                reply_markup=InlineKeyboardMarkup(buttons)
            )
