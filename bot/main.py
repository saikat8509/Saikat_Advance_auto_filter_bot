# bot/__main__.py

import asyncio
import logging
from pyrogram import Client
from bot import plugins
from config import API_ID, API_HASH, BOT_TOKEN, BOT_NAME

# Set up logging
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    level=logging.INFO
)
LOGGER = logging.getLogger(__name__)

# Initialize bot client
bot = Client(
    name=BOT_NAME,
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins={"root": "bot/plugins"}
)

async def main():
    try:
        await bot.start()
        LOGGER.info(f"{BOT_NAME} started successfully.")
        print(f"\n🚀 {BOT_NAME} is now running!\n")
        await idle()
    except Exception as e:
        LOGGER.error(f"An error occurred while starting the bot: {e}")
    finally:
        await bot.stop()
        LOGGER.info(f"{BOT_NAME} stopped.")

if __name__ == "__main__":
    from pyrogram.idle import idle
    asyncio.run(main())
