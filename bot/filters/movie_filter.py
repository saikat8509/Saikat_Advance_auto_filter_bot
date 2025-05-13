# bot/filters/movie_filter.py

from aiogram.types import Message
from aiogram.filters import BaseFilter
import re

class MovieFilter(BaseFilter):
    """
    Filter that checks whether the user's message looks like a movie name request.
    Used for triggering autofilter responses.
    """

    def __init__(self, min_length: int = 3):
        self.min_length = min_length

    async def __call__(self, message: Message) -> bool:
        # Skip messages that are commands
        if message.text and message.text.startswith(('/', '!', '.', '#')):
            return False

        # Check that it's not a reply, has reasonable length, and contains at least some alphabet
        if (
            message.text and
            len(message.text.strip()) >= self.min_length and
            not message.reply_to_message and
            re.search(r"[a-zA-Z]", message.text)
        ):
            return True

        return False
