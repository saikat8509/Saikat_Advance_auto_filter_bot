# bot/plugins/url_shortener.py

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from database.users import is_premium_user
from utils.shortener import generate_short_url
from utils.premium import get_premium_prompt
from config import TUTORIAL_CHANNEL, SHORTEN_DOMAINS

@Client.on_message(filters.command("shorturl") & filters.private)
async def url_shortener_handler(client: Client, message: Message):
    user_id = message.from_user.id
    args = message.text.split(" ", 1)

    if len(args) != 2:
        await message.reply_text(
            "❗️ Usage:\n`/shorturl https://example.com/long-link`",
            quote=True
        )
        return

    original_url = args[1]

    if await is_premium_user(user_id):
        await message.reply_text(
            f"💎 You are a premium user!\n\n🔗 Here’s your direct link:\n`{original_url}`",
            quote=True
        )
        return

    shortened_url = await generate_short_url(original_url, user_id)

    await message.reply_photo(
        photo="https://graph.org/file/123abc456def7890.png",  # Replace with your graph.org URL
        caption=(
            f"🎯 **Shortened Link Generated!**\n\n"
            f"{get_premium_prompt()}\n\n"
            f"🔗 Link: `{shortened_url}`"
        ),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🚀 Download Now", url=shortened_url)],
            [
                InlineKeyboardButton("💎 Buy Premium", callback_data="buy_premium"),
                InlineKeyboardButton("📽 How To Download", url=TUTORIAL_CHANNEL)
            ]
        ])
    )
