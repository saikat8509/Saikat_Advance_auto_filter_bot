from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime, time, timedelta
import pytz
import asyncio

# Example db placeholder - replace with your actual DB instance
db = None  # TODO: replace with actual db client (e.g., Motor for MongoDB)

# Timezones example - you may want to store user timezones in db or infer from Telegram (if possible)
DEFAULT_TIMEZONE = "UTC"


# Graph.org image URLs for wishes
WISH_IMAGES = {
    "morning": "https://graph.org/file/morning_image.png",    # Replace with your actual graph.org images
    "afternoon": "https://graph.org/file/afternoon_image.png",
    "evening": "https://graph.org/file/evening_image.png",
    "night": "https://graph.org/file/night_image.png",
}

# Static wish texts
WISH_TEXTS = {
    "morning": "🌅 Good Morning! Have a bright and joyful day ahead!",
    "afternoon": "☀️ Good Afternoon! Hope your day is going great!",
    "evening": "🌇 Good Evening! Relax and enjoy your evening!",
    "night": "🌙 Good Night! Sleep well and sweet dreams!",
}


def get_current_period(user_tz: str) -> str:
    """
    Determine which period of the day it currently is in the user's timezone.
    Returns one of "morning", "afternoon", "evening", "night".
    """

    try:
        tz = pytz.timezone(user_tz)
    except Exception:
        tz = pytz.timezone(DEFAULT_TIMEZONE)

    now = datetime.now(tz).time()

    if time(5, 0) <= now < time(12, 0):
        return "morning"
    elif time(12, 0) <= now < time(16, 0):
        return "afternoon"
    elif time(16, 0) <= now < time(20, 0):
        return "evening"
    else:
        return "night"


async def send_wish(client: Client, chat_id: int, period: str):
    """
    Send the wish message with image and text for the given period to the chat.
    """

    image_url = WISH_IMAGES.get(period)
    text = WISH_TEXTS.get(period)

    # Inline keyboard with "More Wishes" and "Home" buttons
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("🎉 More Wishes", callback_data="show_wishes_menu"),
                InlineKeyboardButton("🏠 Home", callback_data="start_back_cb"),
            ]
        ]
    )

    # Send photo with caption
    await client.send_photo(
        chat_id=chat_id,
        photo=image_url,
        caption=text,
        reply_markup=keyboard,
    )


@Client.on_message(filters.command("wish") & filters.private)
async def manual_wish_command(client: Client, message: Message):
    """
    /wish command sends a wish according to the user's timezone.
    Optionally, accepts an argument: /wish morning|afternoon|evening|night
    """

    user = message.from_user
    user_tz = None

    # You can extend to fetch user's timezone from db here
    # For now, defaulting to UTC
    user_tz = DEFAULT_TIMEZONE

    period = None

    # Check if user supplied an argument
    if len(message.command) > 1:
        arg = message.command[1].lower()
        if arg in WISH_TEXTS:
            period = arg

    if not period:
        period = get_current_period(user_tz)

    await send_wish(client, message.chat.id, period)


@Client.on_callback_query(filters.regex("^show_wishes_menu$"))
async def wishes_menu_callback(client: Client, callback_query):
    """
    Shows a menu to manually select wish type.
    """

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Good Morning ☀️", callback_data="wish_morning"),
                InlineKeyboardButton("Good Afternoon ☀️", callback_data="wish_afternoon"),
            ],
            [
                InlineKeyboardButton("Good Evening 🌆", callback_data="wish_evening"),
                InlineKeyboardButton("Good Night 🌙", callback_data="wish_night"),
            ],
            [
                InlineKeyboardButton("🏠 Home", callback_data="start_back_cb"),
            ],
        ]
    )

    await callback_query.message.edit_text(
        "Select a wish to send:",
        reply_markup=keyboard,
    )
    await callback_query.answer()


@Client.on_callback_query(
    filters.regex(r"^wish_(morning|afternoon|evening|night)$")
)
async def send_selected_wish_callback(client: Client, callback_query):
    """
    Send the wish selected from the menu.
    """

    period = callback_query.data.split("_")[1]
    chat_id = callback_query.message.chat.id

    await send_wish(client, chat_id, period)
    await callback_query.answer(f"Sent {period.capitalize()} wish!")


async def auto_wish_users(client: Client):
    """
    Periodic task to auto-send wishes to users based on their timezone.
    To be run as a background task or cron job.
    """

    if not db:
        print("DB not configured for auto_wish_users.")
        return

    # Fetch all users and their timezone from db
    users = await db.users.find({}).to_list(length=None)

    now_utc = datetime.utcnow()

    for user in users:
        try:
            user_id = user.get("user_id")
            user_tz = user.get("timezone", DEFAULT_TIMEZONE)
            last_wish_sent = user.get("last_wish_sent")  # datetime stored in UTC

            tz = pytz.timezone(user_tz)
            now_local = datetime.now(tz)

            period = get_current_period(user_tz)

            # Logic: Send wish only once per period per day
            # If last wish sent is None or before today period, send wish

            if last_wish_sent:
                last_sent_local = last_wish_sent.astimezone(tz)
                if last_sent_local.date() == now_local.date():
                    # Wish already sent today
                    continue

            # Send wish
            await send_wish(client, user_id, period)

            # Update last wish sent in DB
            await db.users.update_one(
                {"user_id": user_id},
                {"$set": {"last_wish_sent": datetime.utcnow()}},
                upsert=True,
            )

            # Add small delay to avoid flooding
            await asyncio.sleep(1)

        except Exception as e:
            print(f"Failed to send wish to user {user.get('user_id')}: {e}")


# You can schedule auto_wish_users() to run periodically via an external scheduler or asyncio tasks
# e.g., asyncio.create_task(auto_wish_users(client)) after startup

