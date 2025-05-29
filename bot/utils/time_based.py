from datetime import datetime, time
import pytz
from bot.config import WISHES

def get_time_of_day(hour: int) -> str:
    """
    Determine the time of day category from an hour integer (0-23).
    Returns one of: 'morning', 'afternoon', 'evening', 'night'.
    """
    if 5 <= hour < 12:
        return "morning"
    elif 12 <= hour < 17:
        return "afternoon"
    elif 17 <= hour < 21:
        return "evening"
    else:
        return "night"

def get_wish_for_timezone(timezone_str: str) -> dict:
    """
    Given a timezone string (e.g., 'Asia/Kolkata'), return a dict with:
    - 'text': the wish text for current local time,
    - 'image_url': the corresponding image URL for that time of day.

    If timezone is invalid or not provided, defaults to UTC.
    """
    try:
        tz = pytz.timezone(timezone_str)
    except Exception:
        tz = pytz.UTC

    now = datetime.now(tz)
    tod = get_time_of_day(now.hour)

    # WISHES dictionary from config should have keys like 'morning', 'afternoon', etc.
    wish_text = WISHES.get(tod, {}).get("text", "Hello!")
    image_url = WISHES.get(tod, {}).get("image_url", "")

    return {
        "text": wish_text,
        "image_url": image_url,
        "time_of_day": tod,
        "time": now.strftime("%H:%M")
    }
