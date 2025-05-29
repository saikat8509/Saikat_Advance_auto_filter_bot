import asyncio
import logging
from pyrogram import Client, idle
from bot.utils.log import configure_logging
from config import API_ID, API_HASH, BOT_TOKEN, BOT_NAME, OWNER_USERNAME

# Configure logging
configure_logging()
LOGGER = logging.getLogger(__name__)

# Bot Client
app = Client(
    name=BOT_NAME,
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workers=100,
    plugins={"root": "bot.handlers"},
)

# Startup routine
async def startup_checks():
    from bot.utils.database import init_db
    from bot.utils.fsub_check import check_fsub_channels

    LOGGER.info("Initializing database...")
    await init_db()

    LOGGER.info("Verifying Force Subscribe channels...")
    await check_fsub_channels()

    LOGGER.info("Startup checks complete.")

# Main async runner
async def main():
    await startup_checks()
    await app.start()
    LOGGER.info("Bot started successfully as @%s", (await app.get_me()).username)
    await idle()
    await app.stop()
    LOGGER.info("Bot stopped. Goodbye!")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        LOGGER.info("Bot stopped manually.")
    except Exception as e:
        LOGGER.exception("Fatal error: %s", str(e))
