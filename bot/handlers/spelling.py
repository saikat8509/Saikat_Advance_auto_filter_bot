from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from config import TUTORIAL_CHANNEL_URL, PREMIUM_HEADER
fspelling.py
rom bot.utils.database import (
    get_similar_queries,
    is_premium_user,
    log_search,
)
from bot.plugins.url_shortener import shorten_url
import random

# Optional: fallback text if nothing is found
NO_RESULTS_TEXT = "❌ No similar results found. Try a different search term."

@Client.on_message(filters.command("spelling") & filters.private)
async def spelling_handler(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("Usage: `/spelling <search term>`", quote=True)

    query = message.text.split(" ", 1)[1].strip()
    user_id = message.from_user.id
    is_premium = await is_premium_user(user_id)

    # Log the search
    await log_search(user_id, query)

    # Get spelling suggestions (from database or custom logic)
    suggestions = await get_similar_queries(query)

    if not suggestions:
        return await message.reply_text(NO_RESULTS_TEXT, quote=True)

    buttons = []
    for suggestion in suggestions[:10]:  # Limit to top 10
        if is_premium:
            # Premium users get direct file link
            buttons.append([
                InlineKeyboardButton(text=suggestion, callback_data=f"request#{suggestion}")
            ])
        else:
            # Non-premium users get shortened link with token verification
            shortened = await shorten_url(f"https://t.me/{client.me.username}?start={suggestion.replace(' ', '_')}")
            buttons.append([
                InlineKeyboardButton(text=suggestion, url=shortened)
            ])

    # Add tutorial/help link for non-premium
    if not is_premium:
        buttons.append([
            InlineKeyboardButton("❓ How To Download", url=TUTORIAL_CHANNEL_URL)
        ])

    await message.reply_photo(
        photo=random.choice(PREMIUM_HEADER.split("\n")),  # or a spelling banner image from config
        caption="🔍 **Did you mean:**",
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode="markdown"
    )
