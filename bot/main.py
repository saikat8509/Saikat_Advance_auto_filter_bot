# bot/main.py

import logging
from pyrogram import Client, filters, idle
from bot.config import (
    API_ID, API_HASH, BOT_TOKEN, PLUGIN_PATH, LOG_CHANNEL
)

from bot.database import db
from bot.handlers import (
    start, filters_handler, admin, subscription, premium,
    broadcast, verify_handler, wishes
)
from bot.utils.helpers import load_wishes_job

# Logging setup
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
LOGGER = logging.getLogger(__name__)

# Bot client instance
Bot = Client(
    "AutoFilterBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins={"root": PLUGIN_PATH}
)

# Global startup logic
async def startup_tasks():
    # MongoDB connection check
    if await db.test_connection():
        LOGGER.info("✅ MongoDB connection successful.")
    else:
        LOGGER.warning("⚠️ MongoDB connection failed.")

    # Load time-based wishes scheduler
    load_wishes_job(Bot)

    # Send startup log
    try:
        await Bot.send_message(LOG_CHANNEL, "✅ Bot started successfully!")
    except Exception as e:
        LOGGER.warning(f"Failed to send startup log message: {e}")

# Main runner
async def main():
    await Bot.start()
    LOGGER.info("🚀 Bot is running...")
    await startup_tasks()
    await idle()
    await Bot.stop()
    LOGGER.info("🛑 Bot stopped.")

# Entry point
if __name__ == "__main__":
    import asyncio
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        LOGGER.info("Bot stopped manually.")
