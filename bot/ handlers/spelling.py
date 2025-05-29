from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from bot.utils.database import db

# For spelling correction, using TextBlob or you can customize this.
# Install via: pip install textblob
from textblob import TextBlob

# Optional: You can implement caching, user limits, or premium check with db

@Client.on_message(filters.command("spelling") & filters.private)
async def spelling_handler(client: Client, message: Message):
    """
    Handle /spelling command in private chat.
    Usage: /spelling <text>
    Replies with corrected spelling.
    """

    user_id = message.from_user.id
    text = message.text

    # Extract the text to check
    parts = text.split(None, 1)
    if len(parts) < 2:
        await message.reply_text(
            "Please provide the text to check.\n\nUsage: `/spelling your_text_here`",
            parse_mode="markdown",
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("Help", callback_data="help_spelling")]
                ]
            )
        )
        return

    user_text = parts[1].strip()
    if not user_text:
        await message.reply_text("Please provide valid text to check spelling.")
        return

    # Optional: Log user query or usage count
    await db.add_user(user_id)  # make sure user is tracked

    # Spell correction using TextBlob
    blob = TextBlob(user_text)
    corrected_text = str(blob.correct())

    if corrected_text.lower() == user_text.lower():
        reply_msg = "✅ No spelling mistakes found!"
    else:
        reply_msg = f"📝 **Original:** {user_text}\n\n✅ **Corrected:** {corrected_text}"

    # Reply with the result and buttons for support / groups / more help
    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Support Group", url="https://t.me/Leazy_support_group"),
                InlineKeyboardButton("Movie Group", url="https://t.me/Creazy_Movie_Surch_Group")
            ],
            [
                InlineKeyboardButton("Tutorial Channel", url="https://t.me/How_to_open_file_to_link"),
                InlineKeyboardButton("Update Channel", url="https://t.me/creazy_announcement_hub")
            ],
        ]
    )

    await message.reply_text(reply_msg, parse_mode="markdown", reply_markup=buttons)


# Optional: Callback query handler for help or buttons (if needed)
@Client.on_callback_query(filters.regex("^help_spelling$"))
async def help_spelling_callback(client: Client, callback_query):
    await callback_query.answer()
    await callback_query.message.edit_text(
        "**Spelling Command Help**\n\n"
        "Use `/spelling <text>` to check and correct spelling mistakes in your message.\n\n"
        "Example:\n"
        "`/spelling teh quik brown fox`\n"
        "Will return corrected text.\n\n"
        "If you need further assistance, join our Support Group.",
        parse_mode="markdown",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("Support Group", url="https://t.me/Leazy_support_group")]]
        )
    )
