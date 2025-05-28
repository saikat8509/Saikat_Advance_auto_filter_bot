# handlers/errors.py
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.types import Message
from bot.utils.log import log_exception
import asyncio

@Client.on_message(filters.private)
async def error_handler(client: Client, message: Message):
    try:
        # Place any risky operations here (if any)
        pass
    except FloodWait as e:
        await asyncio.sleep(e.value)
    except Exception as e:
        await log_exception(client, e, context=f"Error triggered by user {message.from_user.id}")
