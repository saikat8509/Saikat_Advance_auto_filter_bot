# bot/main.py

import logging
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from bot.handlers import (
    start,
    help,
    imdb,
    popular,
    premium,
    spelling,
    stats,
    trending,
    wishes
)
from bot.plugins import referral, screenshot, shorten, url_shortener
from bot.utils import (
    database,
    decorators,
    fsub_check,
    time_based,
    ai_spellcheck,
    buttons
)

# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)
logger = logging.getLogger(__name__)

# --- Configuration ---
API_ID = 123456          # Your Telegram API_ID
API_HASH = "your_api_hash_here"  # Your Telegram API_HASH
BOT_TOKEN = "your_bot_token_here" # Your Bot Token

# --- Create Pyrogram Client ---
app = Client(
    "movie_autofilter_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workers=20,             # Parallel workers for concurrency
    sleep_threshold=60      # Automatic reconnect delay
)

# --- Initialize Database ---
db = database.Database()  # Assuming your database.py has a Database class

# --- Startup & Shutdown Events ---
@app.on_startup()
async def startup(client: Client):
    logger.info("Bot is starting up...")
    await db.connect()
    # Add any additional startup tasks here
    logger.info("Database connected and startup complete.")

@app.on_shutdown()
async def shutdown(client: Client):
    logger.info("Bot is shutting down...")
    await db.disconnect()
    logger.info("Database disconnected and shutdown complete.")

# --- Register Command Handlers ---

# /start command
app.add_handler(start.start_handler)

# /help command
app.add_handler(help.help_handler)

# /imdb commands and queries
app.add_handler(imdb.imdb_handler)

# /popular commands
app.add_handler(popular.popular_handler)

# /premium commands
app.add_handler(premium.premium_handler)

# /spelling commands
app.add_handler(spelling.spelling_handler)

# /stats commands
app.add_handler(stats.stats_handler)

# /trending commands
app.add_handler(trending.trending_handler)

# /wishes commands
app.add_handler(wishes.wishes_handler)

# --- Plugin Handlers ---

# Referral plugin
app.add_handler(referral.referral_handler)

# Screenshot plugin for payment verification
app.add_handler(screenshot.screenshot_handler)

# URL shortening plugin
app.add_handler(shorten.shorten_handler)

# URL shortener API integration plugin
app.add_handler(url_shortener.url_shortener_handler)

# --- Filters and Middleware ---

# Force subscribe check middleware
@app.middleware()
async def force_subscribe_check(client: Client, update, next):
    if await fsub_check.is_user_subscribed(client, update):
        return await next()
    else:
        # Send force subscribe message or kick user if needed
        await fsub_check.handle_force_subscribe(client, update)

# AI Spellcheck integration on messages
@app.on_message(filters.text & ~filters.edited)
async def ai_spellcheck_middleware(client: Client, message: Message):
    corrected_text = await ai_spellcheck.check_spelling(message.text)
    if corrected_text and corrected_text != message.text:
        await message.reply_text(f"Did you mean:\n{corrected_text}")

# --- Run the bot ---
if __name__ == "__main__":
    logger.info("Starting the Movie Autofilter Bot...")
    app.run()
