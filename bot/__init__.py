from dotenv import load_dotenv
import os

# Load .env variables
load_dotenv()

# Initialize logging
import logging

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Import Bot & Dispatcher
from pyrogram import Client
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from config import (
    BOT_TOKEN, API_ID, API_HASH,
    PLUGIN_CHANNEL, BOT_USERNAME
)

# Bot client instance
bot = Client(
    name="AutofilterBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="bot/handlers")
)

# Startup Logs
@bot.on_message()
async def bot_started_log(client, message):
    if message.text == "/ping":
        await message.reply("✅ Bot is alive and running.")

# Start scheduled background tasks
from bot.services.scheduler import start_scheduled_jobs

def start_bot():
    logger.info("🚀 Starting Autofilter Bot...")
    start_scheduled_jobs()  # run time-based greetings, post cleanup
    bot.run()

