# bot/handlers/batch.py

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from database.premium_db import is_premium_user
from utils.shortener import generate_short_link
from utils.template import generate_imdb_template
from utils.token import generate_token
from config import TUTORIAL_CHANNEL_LINK

# ✅ /link - For single message/file
@Client.on_message(filters.command("link") & filters.private)
async def link_single_handler(client: Client, message: Message):
    if not message.reply_to_message or not message.reply_to_message.document:
        return await message.reply("❌ Reply to a single movie/document to get its link.")

    user_id = message.from_user.id
    is_premium = await is_premium_user(user_id)

    doc = message.reply_to_message.document
    file_id = doc.file_id
    file_name = doc.file_name

    if is_premium:
        await message.reply(
            f"🎬 **{file_name}**",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("📥 Download Now", url=f"https://t.me/{client.me.username}?start=dl_{file_id}")]]
            ),
        )
    else:
        token = generate_token(file_id, user_id)
        short_link = await generate_short_link(f"https://t.me/{client.me.username}?start={token}")
        await message.reply(
            f"🧲 **{file_name}**\n\n🔐 You are not a premium user. Upgrade for direct access.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("🔥 Buy Premium", callback_data="premium_menu")],
                    [InlineKeyboardButton("📥 Download Now", url=short_link)],
                    [InlineKeyboardButton("❓ How To Download", url=TUTORIAL_CHANNEL_LINK)],
                ]
            ),
        )


# ✅ /batch - For multiple messages
@Client.on_message(filters.command("batch") & filters.private)
async def batch_link_handler(client: Client, message: Message):
    if not message.reply_to_message or not message.reply_to_message.media_group_id:
        return await message.reply("❌ Reply to a media group (album) to batch link all posts.")

    user_id = message.from_user.id
    is_premium = await is_premium_user(user_id)

    media_group_id = message.reply_to_message.media_group_id
    album = await client.get_messages(chat_id=message.chat.id, message_ids=list(range(message.reply_to_message.id - 10, message.reply_to_message.id + 10)))

    valid_docs = [msg for msg in album if msg.media_group_id == media_group_id and msg.document]

    if not valid_docs:
        return await message.reply("❌ No valid files found in this media group.")

    batch_buttons = []
    for msg in valid_docs:
        file_id = msg.document.file_id
        file_name = msg.document.file_name
        if is_premium:
            url = f"https://t.me/{client.me.username}?start=dl_{file_id}"
        else:
            token = generate_token(file_id, user_id)
            url = await generate_short_link(f"https://t.me/{client.me.username}?start={token}")
        batch_buttons.append([InlineKeyboardButton(file_name[:50], url=url)])

    caption = "📦 **Batch File Links Generated!**\n\n" + ("🚀 You are a premium user." if is_premium else "🔐 Non-premium users get short links.")

    if not is_premium:
        batch_buttons.append([InlineKeyboardButton("🔥 Buy Premium", callback_data="premium_menu")])
        batch_buttons.append([InlineKeyboardButton("❓ How To Download", url=TUTORIAL_CHANNEL_LINK)])

    await message.reply(
        caption,
        reply_markup=InlineKeyboardMarkup(batch_buttons),
        disable_web_page_preview=True,
    )
