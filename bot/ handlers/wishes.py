from pyrogram import Client, filters
from pyrogram.types import Message, InputMediaPhoto
from datetime import datetime
from config import WISHES
import pytz

# Mapping static wish commands to config keys
STATIC_WISHES = {
    "goodmorning": "morning",
    "goodafternoon": "afternoon",
    "goodevening": "evening",
    "goodnight": "night"
}

def get_current_wish_by_timezone(timezone="Asia/Kolkata"):
    try:
        now = datetime.now(pytz.timezone(timezone))
        hour = now.hour
        if 4 <= hour < 12:
            return "morning"
        elif 12 <= hour < 17:
            return "afternoon"
        elif 17 <= hour < 21:
            return "evening"
        else:
            return "night"
    except Exception:
        return None

@Client.on_message(filters.command(["wish", "greet", "gm", "auto"]))
async def auto_wish_handler(client: Client, message: Message):
    wish_key = get_current_wish_by_timezone()
    if not wish_key or wish_key not in WISHES:
        return await message.reply("🌐 Unable to determine your wish. Try again later.")

    img_url = WISHES[wish_key].get("image")
    text = WISHES[wish_key].get("text", "🌞 Have a nice day!")

    await message.reply_photo(photo=img_url, caption=text)

@Client.on_message(filters.command(list(STATIC_WISHES.keys())))
async def static_wish_handler(client: Client, message: Message):
    wish_key = STATIC_WISHES[message.command[0].lower()]
    config = WISHES.get(wish_key)

    if not config:
        return await message.reply("❌ That wish is not configured.")

    img_url = config.get("image")
    text = config.get("text", "🌞 Have a good day!")

    await message.reply_photo(photo=img_url, caption=text)
