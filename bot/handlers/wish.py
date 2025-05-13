# bot/handlers/wish.py

import datetime
from pyrogram import Client
from config import (
    MOVIE_GROUP_ID,
    GOOD_MORNING_STICKER,
    GOOD_AFTERNOON_STICKER,
    GOOD_EVENING_STICKER,
    GOOD_NIGHT_STICKER,
)

# Wish messages
WISH_MESSAGES = {
    "morning": "🌅 **Good Morning Movie Lovers!**\n\n☕ Grab your coffee and enjoy the fresh movies 🍿🎬",
    "afternoon": "☀️ **Good Afternoon Cinephiles!**\n\n🍿 Take a break and enjoy your favorite flick!",
    "evening": "🌇 **Good Evening Film Fans!**\n\n🎞️ Time to relax with your favorite movies!",
    "night": "🌙 **Good Night Streamers!**\n\n📽️ End the day with a blockbuster hit!"
}

# Time ranges (24-hour format)
TIME_RANGES = {
    "morning": range(5, 12),
    "afternoon": range(12, 17),
    "evening": range(17, 21),
    "night": list(range(21, 24)) + list(range(0, 5)),
}

# Corresponding stickers
STICKERS = {
    "morning": GOOD_MORNING_STICKER,
    "afternoon": GOOD_AFTERNOON_STICKER,
    "evening": GOOD_EVENING_STICKER,
    "night": GOOD_NIGHT_STICKER,
}


async def send_time_based_wish(bot: Client):
    """Determine the current time and send the appropriate wish message and sticker to the movie group."""
    hour = datetime.datetime.now().hour

    for period, hours in TIME_RANGES.items():
        if hour in hours:
            message = WISH_MESSAGES.get(period)
            sticker = STICKERS.get(period)

            try:
                # Send sticker
                if sticker:
                    await bot.send_sticker(chat_id=MOVIE_GROUP_ID, sticker=sticker)

                # Send message
                await bot.send_message(chat_id=MOVIE_GROUP_ID, text=message)
            except Exception as e:
                print(f"[WISH_SEND_ERROR] {e}")

            break


