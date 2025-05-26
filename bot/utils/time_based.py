# bot/utils/time_based.py

from datetime import datetime
import pytz

# Fallback timezone in case user timezone is unknown
DEFAULT_TIMEZONE = "Asia/Kolkata"

def get_current_time(timezone: str = DEFAULT_TIMEZONE) -> datetime:
    """
    Returns the current datetime object based on a given timezone.
    """
    try:
        tz = pytz.timezone(timezone)
        return datetime.now(tz)
    except Exception:
        return datetime.now(pytz.timezone(DEFAULT_TIMEZONE))

def get_time_period(timezone: str = DEFAULT_TIMEZONE) -> str:
    """
    Determines the time period (morning, afternoon, evening, night) based on user's timezone.
    """
    now = get_current_time(timezone).hour

    if 5 <= now < 12:
        return "morning"
    elif 12 <= now < 17:
        return "afternoon"
    elif 17 <= now < 21:
        return "evening"
    else:
        return "night"

def get_wish_text(timezone: str = DEFAULT_TIMEZONE) -> tuple:
    """
    Returns appropriate wish text and associated static image URL for the time of day.
    """
    period = get_time_period(timezone)

    if period == "morning":
        return "🌞 Good Morning! Have a great day ahead!", "https://graph.org/file/morning_image.jpg"
    elif period == "afternoon":
        return "☀️ Good Afternoon! Stay productive!", "https://graph.org/file/afternoon_image.jpg"
    elif period == "evening":
        return "🌇 Good Evening! Hope you had a nice day!", "https://graph.org/file/evening_image.jpg"
    else:
        return "🌙 Good Night! Sweet dreams!", "https://graph.org/file/night_image.jpg"

def is_time_for_greeting(user_id: int, last_sent_time: datetime, timezone: str = DEFAULT_TIMEZONE) -> bool:
    """
    Checks whether enough time has passed (e.g., 6 hours) since the last greeting to avoid spamming.
    """
    current_time = get_current_time(timezone)
    if not last_sent_time:
        return True

    delta = current_time - last_sent_time
    return delta.total_seconds() > 6 * 3600  # 6 hours
