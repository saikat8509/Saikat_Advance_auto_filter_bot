from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from spellchecker import SpellChecker

# Initialize SpellChecker instance (English)
spell = SpellChecker()

# Command: /spellcheck <text>
# Usage: User sends /spellcheck followed by text to check spelling errors
@Client.on_message(filters.command("spellcheck") & filters.private)
async def spellcheck_handler(client: Client, message: Message):
    # Extract text after command
    text = message.text
    parts = text.split(maxsplit=1)

    if len(parts) < 2:
        await message.reply_text("❗ Please provide text to check spelling.\n\nUsage:\n/spellcheck your text here")
        return

    text_to_check = parts[1]

    # Tokenize words and find misspelled words
    words = text_to_check.split()
    misspelled = spell.unknown(words)

    if not misspelled:
        await message.reply_text("✅ No spelling mistakes found!")
        return

    # Generate suggestions for each misspelled word
    response = "**Spelling Check Results:**\n\n"
    for word in misspelled:
        suggestions = spell.candidates(word)
        # Limit suggestions to top 3
        suggestions = list(suggestions)[:3]
        response += f"❌ `{word}`\n➡️ Suggestions: {', '.join(suggestions)}\n\n"

    # Reply with inline button to usage tutorial if needed
    await message.reply_text(
        response,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("📚 How to Use", url="https://t.me/How_to_open_file_to_link")]]
        ),
        parse_mode="md",
        disable_web_page_preview=True
    )

# Optional: inline query support to suggest spelling corrections inline
@Client.on_inline_query()
async def inline_spell_suggestions(client: Client, inline_query):
    query = inline_query.query.strip()
    if not query:
        await inline_query.answer(results=[], cache_time=0)
        return

    words = query.split()
    misspelled = spell.unknown(words)
    if not misspelled:
        await inline_query.answer(results=[], cache_time=0)
        return

    from pyrogram.types import InlineQueryResultArticle, InputTextMessageContent

    results = []
    for word in misspelled:
        suggestions = list(spell.candidates(word))[:3]
        text = f"Suggestions for '{word}': {', '.join(suggestions)}"
        results.append(
            InlineQueryResultArticle(
                title=f"Correct '{word}'",
                input_message_content=InputTextMessageContent(text),
                description=text,
                thumb_url="https://graph.org/file/abcdef1234567890.png"  # Replace with relevant icon URL
            )
        )
    await inline_query.answer(results=results, cache_time=30, is_personal=True)

