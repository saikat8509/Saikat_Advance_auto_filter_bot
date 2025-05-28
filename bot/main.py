import logging
from pyrogram import Client
from config import BOT_TOKEN, API_ID, API_HASH
from bot import handlers  # Ensure all handlers are imported in bot/__init__.py

# Logging Configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# Bot Initialization
app = Client(
    "autofilter-bot",
    bot_token=BOT_TOKEN,
    api_id=API_ID,
    api_hash=API_HASH,
    plugins={"root": "bot/handlers"}
)

if __name__ == "__main__":
    logger.info("🚀 Bot starting...")
    app.run()
