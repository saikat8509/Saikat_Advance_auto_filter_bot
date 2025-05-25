# bot/plugins/shorten.py

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from database.users import is_premium_user
from utils.shortener import generate_short_url
from utils.premium import get_premium_prompt
from config import TUTORIAL_CHANNEL, SHORTEN_DOMAINS

@Client.on_message(filters.private & filters.command("shorten"))
async def shorten_handler(client: Client, message: Message):
    user_id = message.from_user.id
    args = message.text.split(" ", 1)

    if len(args) != 2:
        return await message.reply_text(
            "❗️ Send a valid command like:\n`/shorten https://example.com/longlink`",
            quote=True
        )

    original_url = args[1]

    # Check if user is premium
    if await is_premium_user(user_id):
        await message.reply_text(f"🚀 *Premium User*\nHere’s your direct link:\n{original_url}")
        return

    # Generate short link with token verification for non-premium user
    short_url = await generate_short_url(original_url, user_id)

    # Premium ad template (with graph.org image)
    premium_message = get_premium_prompt()

    await message.reply_photo(
        photo="https://graph.org/file/123abc456def7890.png",  # Replace with your image
        caption=(
            f"**🔗 Your Shortened Link**\n\n"
            f"{premium_message}\n\n"
            f"🧷 Link: `{short_url}`\n\n"
            f"⚡️ Fast | Safe | Tracked"
        ),
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("⬇️ Download Now", url=short_url)
            ],
            [
                InlineKeyboardButton("🎖 Buy Premium", callback_data="buy_premium"),
                InlineKeyboardButton("📽 How To Download", url=TUTORIAL_CHANNEL)
            ]
        ])
    )
