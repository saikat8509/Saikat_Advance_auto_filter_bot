# handlers/filters.py

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from database.file_data import get_filtered_files
from utils.helpers import generate_imdb_template
from config import ENABLE_FILTERS, ENABLE_LANGUAGE_FILTER, ENABLE_SEASON_FILTER, ENABLE_QUALITY_FILTER, ENABLE_EPISODE_FILTER, ENABLE_YEAR_FILTER

# This will handle automatic file filtering by keywords like language, season, quality, etc.
@Client.on_message(filters.command("filter") & filters.text)
async def auto_filter(client: Client, message: Message):
    if not ENABLE_FILTERS:
        return await message.reply("Filters are currently disabled by the admin.")

    filters_applied = []
    
    if ENABLE_LANGUAGE_FILTER and "language" in message.text.lower():
        filters_applied.append("Language Filter")
    if ENABLE_SEASON_FILTER and "season" in message.text.lower():
        filters_applied.append("Season Filter")
    if ENABLE_QUALITY_FILTER and "quality" in message.text.lower():
        filters_applied.append("Quality Filter")
    if ENABLE_EPISODE_FILTER and "episode" in message.text.lower():
        filters_applied.append("Episode Filter")
    if ENABLE_YEAR_FILTER and "year" in message.text.lower():
        filters_applied.append("Year Filter")

    if not filters_applied:
        return await message.reply("No valid filter found in your message.")
    
    # Simulate fetching filtered results from the database (based on applied filters)
    filtered_files = await get_filtered_files(filters_applied)
    
    if not filtered_files:
        return await message.reply("No files found for the applied filters.")
    
    # Create the inline keyboard based on the filter results
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("View Files", callback_data="view_files")]
    ])
    
    # Prepare the template for the filtered files (could use an IMDb message template)
    imdb_message = await generate_imdb_template(filtered_files)
    
    # Send filtered message with results and keyboard
    await message.reply(imdb_message, reply_markup=keyboard)

# Manual file filtering (Admin only)
@Client.on_message(filters.command("manual_filter") & filters.user(ADMINS))
async def manual_filter(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply("Please provide the filter parameters (e.g., /manual_filter language: English quality: HD).")
    
    filter_criteria = message.text.split(" ")[1:]
    filters_applied = []

    for criteria in filter_criteria:
        if "language" in criteria:
            filters_applied.append("Language Filter")
        if "season" in criteria:
            filters_applied.append("Season Filter")
        if "quality" in criteria:
            filters_applied.append("Quality Filter")
        if "episode" in criteria:
            filters_applied.append("Episode Filter")
        if "year" in criteria:
            filters_applied.append("Year Filter")

    if not filters_applied:
        return await message.reply("Invalid filter criteria.")
    
    # Fetch files based on manual filters
    filtered_files = await get_filtered_files(filters_applied)
    
    if not filtered_files:
        return await message.reply("No files match the manual filter criteria.")
    
    # Send filtered files with detailed message
    imdb_message = await generate_imdb_template(filtered_files)
    await message.reply(imdb_message)

