from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import POPULAR_CHANNEL_ID

@Client.on_message(filters.command("popular"))
async def popular_handler(client: Client, message: Message):
    try:
        popular_channel_id = POPULAR_CHANNEL_ID
        if not popular_channel_id:
            return await message.reply("❌ Popular channel not configured.")

        # Forward recent media from the popular channel (latest 10 messages with media)
        messages = []
        async for msg in client.get_chat_history(popular_channel_id, limit=20):
            if msg.media:
                messages.append(msg)
            if len(messages) >= 10:
                break

        if not messages:
            return await message.reply("⚠️ No popular files found in the channel.")

        await message.reply_text(
            "📊 **Popular Files:**",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("🔁 Refresh", callback_data="refresh_popular")]]
            )
        )

        for msg in messages:
            await msg.copy(chat_id=message.chat.id)

    except Exception as e:
        await message.reply(f"🚫 Error fetching popular content:\n`{e}`")

@Client.on_callback_query(filters.regex("refresh_popular"))
async def refresh_popular_callback(client, callback_query):
    try:
        popular_channel_id = POPULAR_CHANNEL_ID
        if not popular_channel_id:
            return await callback_query.answer("❌ Popular channel not configured.", show_alert=True)

        messages = []
        async for msg in client.get_chat_history(popular_channel_id, limit=20):
            if msg.media:
                messages.append(msg)
            if len(messages) >= 10:
                break

        if not messages:
            return await callback_query.answer("⚠️ No popular content found.", show_alert=True)

        await callback_query.answer("🔄 Popular files refreshed!")
        for msg in messages:
            await msg.copy(chat_id=callback_query.message.chat.id)

    except Exception as e:
        await callback_query.message.reply(f"🚫 Error:\n`{e}`")
