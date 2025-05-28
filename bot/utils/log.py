from pyrogram import Client
from config import LOG_CHANNEL

async def log_to_channel(bot: Client, message: str):
    """Send a text log to the log channel."""
    try:
        await bot.send_message(LOG_CHANNEL, text=message)
    except Exception as e:
        print(f"[LOG ERROR] Failed to log to channel: {e}")


async def log_exception(bot: Client, exception: Exception, context: str = ""):
    """Log an exception with optional context."""
    text = f"⚠️ <b>Exception Occurred</b>\n\n<b>Context:</b> <code>{context}</code>\n<b>Error:</b> <code>{exception}</code>"
    await log_to_channel(bot, text)
