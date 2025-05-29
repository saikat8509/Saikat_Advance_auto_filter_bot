from pyrogram import Client, filters
from pyrogram.types import Message
from bot.utils.database import db

# You can replace or integrate any spelling correction library here
# For this example, I'll use 'textblob' for spelling correction
# If you want me to add a custom spell check or other, just say!

try:
    from textblob import TextBlob
except ImportError:
    # TextBlob not installed, install or use another library
    pass

@Client.on_message(filters.command("spellcheck") & filters.private)
async def spellcheck_handler(client: Client, message: Message):
    """
    Handler for /spellcheck command.
    Corrects spelling errors in the provided text.
    Usage: /spellcheck your text here
    """
    if len(message.command) < 2:
        await message.reply_text("❌ Please provide some text to spellcheck.\n\nUsage:\n/spellcheck your text here")
        return

    text_to_check = message.text.split(None, 1)[1]

    # Basic spell correction using TextBlob
    try:
        corrected_text = str(TextBlob(text_to_check).correct())
    except Exception as e:
        await message.reply_text(f"⚠️ An error occurred while checking spelling:\n{e}")
        return

    if corrected_text.lower() == text_to_check.lower():
        reply = "✅ No spelling mistakes found!"
    else:
        reply = f"✏️ Corrected Text:\n\n{corrected_text}"

    # Optional: Log user usage for stats (if you want)
    await db.add_user(message.from_user.id)

    await message.reply_text(reply)


@Client.on_message(filters.command("spellhelp") & filters.private)
async def spellhelp_handler(client: Client, message: Message):
    """
    Handler to show help for spelling commands.
    """
    help_text = (
        "**Spellcheck Command Help**\n\n"
        "Use the `/spellcheck` command followed by the text you want to check.\n\n"
        "**Example:**\n"
        "`/spellcheck This is a smple txt with errrs.`\n\n"
        "The bot will reply with the corrected text."
    )
    await message.reply_text(help_text)
