from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import REQUEST_CHANNEL_ID
from bot.utils.decorators import is_user_banned

# Allow users to request a movie using: #request <movie name>
@Client.on_message(filters.command(["request", "req"]) | filters.regex(r"^#request", flags=re.IGNORECASE))
@is_user_banned
async def handle_request_command(client: Client, message: Message):
    user = message.from_user
    query = (
        message.text.split(" ", 1)[1].strip()
        if len(message.text.split()) > 1 else None
    )

    if not query:
        return await message.reply("❗ Please use: `/request <movie name>`", quote=True)

    request_text = (
        f"📥 **New Request Received**\n\n"
        f"👤 User: [{user.first_name}](tg://user?id={user.id})\n"
        f"🆔 User ID: `{user.id}`\n"
        f"📝 Request: `{query}`"
    )

    if REQUEST_CHANNEL_ID:
        try:
            await client.send_message(
                chat_id=REQUEST_CHANNEL_ID,
                text=request_text
            )
            await message.reply(
                "✅ Your request has been sent to the admin team.\n"
                "We’ll try to add the content soon!",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("🏷 Request Channel", url=f"https://t.me/{REQUEST_CHANNEL_ID.lstrip('@')}")]]
                ),
                quote=True
            )
        except Exception as e:
            await message.reply("❌ Failed to send your request. Try again later.")
    else:
        await message.reply("❌ Request feature is disabled.", quote=True)

