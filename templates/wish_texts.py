# templates/wish_texts.py

from config import WISHES

def get_wish_text_and_image(time_of_day: str) -> tuple[str, str]:
    """
    Returns the wish text and image URL for a given time of day.

    Args:
        time_of_day (str): One of "morning", "afternoon", "evening", or "night".

    Returns:
        tuple: (wish_text: str, image_url: str)
    """
    wish = WISHES.get(time_of_day.lower())
    if wish:
        return wish["text"], wish["image"]
    else:
        return "🌟 Hello!", ""
